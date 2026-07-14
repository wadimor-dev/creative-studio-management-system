export const reportSummary = {
  totalTransactions: 145,
  stockIn: 45,
  stockOut: 85,
  return: 12,
  damaged: 3
};

export const reportTransactions = [
  {
    id: 1,
    itemId: 1,
    itemCode: "CAM-001",
    itemName: "Sony A7III Camera",
    type: "OUT",
    quantity: 1,
    user: "Sarah Connor",
    date: "2026-07-07",
    time: "09:15 AM",
    notes: "Project Alpha"
  },
  {
    id: 2,
    itemId: 2,
    itemCode: "LENS-012",
    itemName: "Sony 24-70mm",
    type: "RETURN",
    quantity: 1,
    user: "John Doe",
    date: "2026-07-07",
    time: "10:30 AM",
    notes: "Returned safely"
  },
  {
    id: 3,
    itemId: 3,
    itemCode: "LIGHT-005",
    itemName: "Godox SL60W",
    type: "IN",
    quantity: 5,
    user: "Admin",
    date: "2026-07-06",
    time: "14:00 PM",
    notes: "New stock arrival"
  },
  {
    id: 4,
    itemId: 5,
    itemCode: "ACC-015",
    itemName: "Manfrotto Tripod",
    type: "DAMAGED",
    quantity: 1,
    user: "Alice Smith",
    date: "2026-07-05",
    time: "16:45 PM",
    notes: "Broken leg lock"
  }
];
