import React, { useMemo } from 'react';
import { hasPermission } from '../../../utils/permissions';

import SidebarItem from './SidebarItem';
import SidebarCollapse from './SidebarCollapse';

const SidebarGroup = ({ group, user }) => {

  const visibleMenus = useMemo(() => {

    return group.children.reduce((result, menu) => {

      // Menu mempunyai submenu
      if (menu.children) {

        const children = menu.children.filter(child =>
          hasPermission(user, child.permission)
        );

        if (children.length > 0) {
          result.push({
            ...menu,
            children
          });
        }

        return result;
      }

      // Menu biasa
      if (hasPermission(user, menu.permission)) {
        result.push(menu);
      }

      return result;

    }, []);

  }, [group, user]);

  if (!visibleMenus.length) return null;

  return (
    <div className="mb-6">

      <h3 className="mb-2 px-3 text-xs font-semibold uppercase tracking-wider text-slate-400">
        {group.title}
      </h3>

      <ul className="space-y-1.5">

        {visibleMenus.map(menu =>

          menu.children
            ? (
              <SidebarCollapse
                key={menu.name}
                item={menu}
              />
            )
            : (
              <SidebarItem
                key={menu.path}
                item={menu}
              />
            )

        )}

      </ul>

    </div>
  );

};

export default SidebarGroup;