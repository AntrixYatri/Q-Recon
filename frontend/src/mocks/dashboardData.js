export const kpiMetrics = {
  totalDocuments: {
    label: 'Total Documents',
    value: '128',
    subtext: '+12 this week',
    trend: 'up',
  },
  verifiedDocuments: {
    label: 'Verified Documents',
    value: '114',
    subtext: '89.1% of total batch',
    trend: 'up',
  },
  activeDiscrepancies: {
    label: 'Active Discrepancies',
    value: '14',
    subtext: '3 high priority',
    trend: 'warning',
  },
  verificationAccuracy: {
    label: 'Verification Accuracy',
    value: '98.4%',
    subtext: 'Tri-source cross-checked',
    trend: 'up',
  },
};

export const weeklyActivityData = [
  { day: 'Mon', verified: 12, total: 14 },
  { day: 'Tue', verified: 18, total: 20 },
  { day: 'Wed', verified: 15, total: 17 },
  { day: 'Thu', verified: 24, total: 26 },
  { day: 'Fri', verified: 21, total: 24 },
  { day: 'Sat', verified: 28, total: 30 },
  { day: 'Sun', verified: 32, total: 35 },
];

export const documentStatusData = [
  { name: 'Verified', count: 114, fill: '#3A801C', description: 'Passed tri-source consistency checks' },
  { name: 'Discrepant', count: 14, fill: '#D4A700', description: 'Requires inspector review' },
  { name: 'Pending', count: 6, fill: '#53B7E8', description: 'Under automated comparison' },
];

export const recentVerifications = [
  {
    packageId: 'RJ-04-102',
    roadScheme: 'NH-62 Junction to Kherapa Road (0-14 km)',
    date: '2026-08-19',
    documents: '3 Files (QCR, Lab, QM)',
    discrepancies: '2 Inconsistencies',
    status: 'Discrepant',
  },
  {
    packageId: 'UP-12-088',
    roadScheme: 'Banda - Baberu Link Road (4-9 km)',
    date: '2026-08-18',
    documents: '3 Files (QCR, Lab, QM)',
    discrepancies: '0 Inconsistencies',
    status: 'Verified',
  },
  {
    packageId: 'MP-07-214',
    roadScheme: 'Rewa - Semariya Rural Corridor (Phase-II)',
    date: '2026-08-17',
    documents: '3 Files (QCR, Lab, QM)',
    discrepancies: '1 Flagged Field',
    status: 'Under Review',
  },
  {
    packageId: 'BR-19-055',
    roadScheme: 'Katihar - Manihari Bypass Connecting Road',
    date: '2026-08-16',
    documents: '3 Files (QCR, Lab, QM)',
    discrepancies: '0 Inconsistencies',
    status: 'Verified',
  },
];
