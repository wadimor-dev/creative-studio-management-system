import React from 'react';
import { NavLink } from 'react-router-dom';

const SidebarItem = ({ item, nested = false }) => {

    const Icon = item.icon;
    const isValidIcon = typeof Icon === 'function' || typeof Icon === 'object';

    return (
        <li>
            <NavLink
                to={item.path}
                className={({ isActive }) => `
                    flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-all
                    ${nested ? 'pl-3' : ''}
                    ${
                        isActive
                            ? 'bg-brand-50 text-brand-600'
                            : 'text-slate-600 hover:bg-slate-50'
                    }
                `}
            >
                {isValidIcon && (
                    <Icon
                        size={nested ? 16 : 20}
                        className="shrink-0"
                    />
                )}

                {item.name}
            </NavLink>
        </li>
    );

};

export default SidebarItem;