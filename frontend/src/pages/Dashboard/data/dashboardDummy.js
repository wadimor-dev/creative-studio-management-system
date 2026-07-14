export const dashboardStats = [
  {
    title: 'Total Items',
    value: '2,845',
    trend: '+12.5%',
    trendUp: true,
    subtitle: 'from last month'
  },
  {
    title: 'Available',
    value: '1,532',
    trend: '+5.2%',
    trendUp: true,
    subtitle: 'ready to use'
  },
  {
    title: 'Borrowed',
    value: '142',
    trend: '-2.4%',
    trendUp: false,
    subtitle: 'currently active'
  },
  {
    title: 'Damaged',
    value: '18',
    trend: '+4.1%',
    trendUp: false,
    subtitle: 'needs repair'
  }
];

export const chartData = [
  { name: 'Jan', borrows: 400, additions: 240 },
  { name: 'Feb', borrows: 300, additions: 139 },
  { name: 'Mar', borrows: 200, additions: 980 },
  { name: 'Apr', borrows: 278, additions: 390 },
  { name: 'May', borrows: 189, additions: 480 },
  { name: 'Jun', borrows: 239, additions: 380 },
  { name: 'Jul', borrows: 349, additions: 430 },
];

export const recentActivities = [
  {
    id: 1,
    user: 'Sarah Connor',
    action: 'borrowed',
    item: 'Sony A7III Camera',
    time: '2 hours ago',
    status: 'pending'
  },
  {
    id: 2,
    user: 'John Doe',
    action: 'returned',
    item: 'MacBook Pro M2',
    time: '4 hours ago',
    status: 'success'
  },
  {
    id: 3,
    user: 'Alice Smith',
    action: 'reported damaged',
    item: 'Tripod Manfrotto',
    time: '1 day ago',
    status: 'danger'
  },
  {
    id: 4,
    user: 'Bob Johnson',
    action: 'borrowed',
    item: 'LED Godox Light',
    time: '2 days ago',
    status: 'success'
  }
];

export const quickSummary = [
  {
    category: 'Most Borrowed',
    title: 'Sony A7III Camera',
    value: '145 times'
  },
  {
    category: 'Most Damaged',
    title: 'Tripod Manfrotto',
    value: '12 times'
  },
  {
    category: 'Most Active User',
    title: 'Sarah Connor',
    value: '45 transactions'
  }
];
