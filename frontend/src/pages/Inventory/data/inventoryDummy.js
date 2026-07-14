export const items = [
  {
    id: 1,
    code: "CAM-001",
    name: "Sony A7III Camera",
    category: "Camera",
    quantity: 5,
    available: 3,
    status: "READY",
    unit: "pcs",
    description: "Full-frame mirrorless camera"
  },
  {
    id: 2,
    code: "LENS-012",
    name: "Sony 24-70mm f/2.8 GM",
    category: "Lens",
    quantity: 3,
    available: 1,
    status: "READY",
    unit: "pcs",
    description: "Standard zoom lens"
  },
  {
    id: 3,
    code: "LIGHT-005",
    name: "Godox SL60W",
    category: "Lighting",
    quantity: 8,
    available: 8,
    status: "READY",
    unit: "pcs",
    description: "LED video light"
  },
  {
    id: 4,
    code: "AUDIO-002",
    name: "Rode Wireless GO II",
    category: "Audio",
    quantity: 4,
    available: 0,
    status: "IN_USE",
    unit: "set",
    description: "Wireless microphone system"
  },
  {
    id: 5,
    code: "ACC-015",
    name: "Manfrotto Tripod",
    category: "Accessories",
    quantity: 10,
    available: 9,
    status: "MAINTENANCE",
    unit: "pcs",
    description: "Heavy duty video tripod, 1 item damaged"
  }
];

export const transactions = [
  {
    id: 1,
    itemId: 1,
    itemCode: "CAM-001",
    itemName: "Sony A7III Camera",
    type: "OUT",
    quantity: 2,
    user: "Sarah Connor",
    date: "2026-07-07",
    notes: "Project Alpha shoot"
  },
  {
    id: 2,
    itemId: 4,
    itemCode: "AUDIO-002",
    itemName: "Rode Wireless GO II",
    type: "OUT",
    quantity: 4,
    user: "John Doe",
    date: "2026-07-06",
    notes: "Interview setup"
  },
  {
    id: 3,
    itemId: 2,
    itemCode: "LENS-012",
    itemName: "Sony 24-70mm f/2.8 GM",
    type: "RETURN",
    quantity: 1,
    user: "Alice Smith",
    date: "2026-07-05",
    notes: "Returned in good condition"
  },
  {
    id: 4,
    itemId: 5,
    itemCode: "ACC-015",
    itemName: "Manfrotto Tripod",
    type: "IN",
    quantity: 5,
    user: "Admin",
    date: "2026-07-01",
    notes: "New purchase restock"
  }
];

export const inventoryStats = [
  {
    title: 'Total Items',
    value: '30',
  },
  {
    title: 'Available',
    value: '21',
  },
  {
    title: 'Borrowed',
    value: '8',
  },
  {
    title: 'Damaged',
    value: '1',
  }
];
