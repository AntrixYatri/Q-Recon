import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

class AnalysisService:
    @staticmethod
    def run_analysis(analysis_id: str, documents: list = None) -> dict:
        """
        Runs comparative cross-document analysis on the documents linked to a project/road.
        """
        try:
            if documents is not None:
                from ai_engine.pipeline import analyze_documents
                raw_results = analyze_documents(documents)
            else:
                from ai_engine.pipeline import run_discrepancy_pipeline
                raw_results = run_discrepancy_pipeline(analysis_id)
            
            discrepancies = []
            
            critical_cnt = 0
            high_cnt = 0
            medium_cnt = 0
            low_cnt = 0
            
            # Legacy counts
            warning_cnt = 0
            minor_cnt = 0
            
            for disc in raw_results.get("discrepancies", []):
                # Canonical representation: uppercase internally, lowercase externally (Task 1)
                sev_upper = str(disc.get("severity", "MEDIUM")).upper()
                mapped_sev = sev_upper.lower()
                
                if mapped_sev == "critical":
                    critical_cnt += 1
                elif mapped_sev == "high":
                    high_cnt += 1
                elif mapped_sev == "medium":
                    medium_cnt += 1
                    warning_cnt += 1
                else:
                    low_cnt += 1
                    minor_cnt += 1

                # Map documents
                docs = []
                for doc in disc.get("documents", []):
                    docs.append({
                        "document_id": doc.get("document_id"),
                        "document_type": doc.get("document_type"),
                        "value": doc.get("value"),
                        "normalized_value": doc.get("normalized_value"),
                        "ocr_confidence": doc.get("ocr_confidence")
                    })

                # Extract legacy doc A and doc B for backward compatibility
                involved_docs = disc.get("documents", [])
                doc_a_name = "Not Specified"
                doc_b_name = "Not Specified"
                val_a = "N/A"
                val_b = "N/A"
                
                if len(involved_docs) >= 1:
                    doc_a_name = f"{involved_docs[0].get('document_type')} ({involved_docs[0].get('document_id')})"
                    val_a = str(involved_docs[0].get("value") or "")
                if len(involved_docs) >= 2:
                    doc_b_name = f"{involved_docs[1].get('document_type')} ({involved_docs[1].get('document_id')})"
                    val_b = str(involved_docs[1].get("value") or "")
                
                # Expose confidence strictly as a float between 0.0 and 1.0 (Task 2)
                conf = float(disc.get("confidence", 0.95))
                if conf > 1.0:
                    conf = conf / 100.0

                discrepancies.append({
                    "id": disc.get("id") or str(disc.get("discrepancy_id", "")),
                    "field": disc.get("field", ""),
                    "discrepancy_type": disc.get("discrepancy_type", ""),
                    "documents": docs,
                    "values": disc.get("values"),
                    "normalized_values": disc.get("normalized_values"),
                    "comparison_status": disc.get("comparison_status"),
                    "difference": disc.get("difference"),
                    "percentage_difference": disc.get("percentage_difference"),
                    "severity": mapped_sev,
                    "severity_reasons": disc.get("severity_reasons"),
                    "confidence": round(conf, 2),
                    "confidence_factors": disc.get("confidence_factors"),
                    "explanation": disc.get("explanation", ""),
                    "metadata": disc.get("metadata"),
                    # Legacy fields
                    "document_a": doc_a_name,
                    "document_b": doc_b_name,
                    "value_a": val_a,
                    "value_b": val_b
                })

            project_details = {
                "road_name": "PMGSY - Shedbal Govt Hospital Link Road (Grounded Synthetic)",
                "package_id": "PRJ-PMGSY-2901002003",
                "district": "Belagavi",
                "state": "Karnataka",
                "data_provenance": {
                    "data_origin": "pmgsy_grounded_synthetic",
                    "source_dataset": "pmgsy_karnataka_100.csv",
                    "source_row_index": 0,
                    "generator": "pmgsy_qcr_generator"
                }
            }

            # Group discrepancies into record groups (Task 7)
            record_groups_dict = {}
            for disc in discrepancies:
                # Use metadata or default
                g_id = "GROUP-1"
                for raw_d in raw_results.get("discrepancies", []):
                    if raw_d.get("id") == disc["id"] or raw_d.get("discrepancy_id") == disc["id"]:
                        g_id = raw_d.get("group_id", "GROUP-1")
                        break
                
                if g_id not in record_groups_dict:
                    record_groups_dict[g_id] = {
                        "group_id": g_id,
                        "documents": [],
                        "discrepancies": []
                    }
                record_groups_dict[g_id]["discrepancies"].append(disc)

            # Extract unique documents per group
            for g_id, group in record_groups_dict.items():
                seen_docs = set()
                for d in group["discrepancies"]:
                    for doc in d.get("documents", []):
                        d_key = (doc["document_id"], doc["document_type"])
                        if d_key not in seen_docs:
                            seen_docs.add(d_key)
                            group["documents"].append({
                                "document_id": doc["document_id"],
                                "document_type": doc["document_type"]
                            })

            record_groups = list(record_groups_dict.values())

            return {
                "analysis_id": analysis_id,
                "project": project_details,
                "processing_status": raw_results.get("processing_status", "success"),
                "documents_analyzed": raw_results.get("documents_analyzed", 3),
                "linked_record_groups": len(record_groups) if record_groups else 1,
                "summary": {
                    "documents_analyzed": raw_results.get("documents_analyzed", 3),
                    "total_discrepancies": len(discrepancies),
                    "critical": critical_cnt,
                    "high": high_cnt,
                    "medium": medium_cnt,
                    "low": low_cnt,
                    # Legacy compatibility
                    "warning": warning_cnt,
                    "minor": minor_cnt
                },
                "discrepancies": discrepancies,
                "record_groups": record_groups
            }

        except Exception as e:
            print(f"[AnalysisService Error] AI pipeline failed: {str(e)}")
            # Fail gracefully, but do not return raw tracebacks (Task 12)
            return {
                "analysis_id": analysis_id,
                "project": {
                    "road_name": "PMGSY - Shedbal Govt Hospital Link Road (Grounded Synthetic)",
                    "package_id": "PRJ-PMGSY-2901002003",
                    "district": "Belagavi",
                    "state": "Karnataka",
                    "data_provenance": {
                        "data_origin": "pmgsy_grounded_synthetic",
                        "source_dataset": "pmgsy_karnataka_100.csv",
                        "source_row_index": 0,
                        "generator": "pmgsy_qcr_generator"
                    }
                },
                "processing_status": "failed",
                "documents_analyzed": 0,
                "linked_record_groups": 0,
                "summary": {
                    "documents_analyzed": 0,
                    "total_discrepancies": 0,
                    "critical": 0,
                    "high": 0,
                    "medium": 0,
                    "low": 0,
                    "warning": 0,
                    "minor": 0
                },
                "discrepancies": [],
                "record_groups": [],
                "error": f"Discrepancy audit failed: {str(e)}"
            }
