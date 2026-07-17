import {
  LayoutDashboard,
  Package,
  Layers,
  FileText,
  Users,
  Settings,
  Briefcase,
  ScanBarcode,
  Activity,
  ClipboardList,
  DatabaseBackup,
} from 'lucide-react';

export default [
  {
    children: [
        {
            name: 'Dashboard',
            icon: LayoutDashboard,
            path: '/dashboard',
            permission: 'DASHBOARD'
        },

    ]    
  },

  {
    title: 'Workspace',

    children: [
        {
            name: 'work',
            icon: ClipboardList,
            path: '/work',
            permission: 'WORK'
        },

    ]
  },

//   {
//     title: 'Inventory',

//     children: [

//         {
//             name: 'Inventory',
//             icon: Package,
//             path: '/inventory',
//             permission: 'INVENTORY'
//         },

//         {
//             name: 'Products',
//             icon: Layers,

//             children: [

//                 {
//                     name: 'Overview',
//                     path: '/products',
//                     permission: 'PRODUCTS'
//                 },

//                 {
//                     name: 'Catalog',
//                     path: '/products/catalog',
//                     permission: 'PRODUCTS'
//                 },

//                 {
//                     name: 'Movements Create',
//                     path: '/products/movements/create',
//                     permission: 'PRODUCTS'
//                 },

//                 {
//                     name: 'Movements',
//                     path: '/products/movements',
//                     permission: 'PRODUCTS'
//                 },

//                 {
//                     name: 'Placements',
//                     path: '/products/placements',
//                     permission: 'PRODUCTS'
//                 },

//                 {
//                     name: 'Barcode Center',
//                     path: '/products/barcode-center',
//                     permission: 'PRODUCTS'
//                 },

//                 {
//                     name: 'Master Data',
//                     path: '/products/master-data',
//                     permission: 'PRODUCTS'
//                 }

//             ]

//         }

//     ]
//   }
];