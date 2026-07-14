import React, { useState, useRef, useEffect } from 'react';
import { Bell, Search, ChevronRight, Menu, LogOut, Settings, User } from 'lucide-react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import Avatar from '../common/Avatar';

const Navbar = ({ onMenuToggle }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const profileRef = useRef(null);

  // Generate simple breadcrumbs from path
  const pathnames = location.pathname.split('/').filter((x) => x);

  // Click outside to close dropdown
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (profileRef.current && !profileRef.current.contains(event.target)) {
        setIsProfileOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleLogout = () => {
    setIsProfileOpen(false);
    logout();
    navigate('/login');
  };

  return (
    <header className="sticky top-0 z-30 flex h-16 w-full items-center justify-between border-b border-slate-200 bg-white/80 px-4 sm:px-6 lg:px-8 backdrop-blur-md">
      
      <div className="flex items-center gap-3">
        {/* Mobile hamburger menu button */}
        <button
          onClick={onMenuToggle}
          className="rounded-lg p-2 text-slate-500 hover:bg-slate-100 hover:text-slate-700 lg:hidden transition-colors focus:outline-none focus:ring-2 focus:ring-brand-500"
          aria-label="Open sidebar menu"
        >
          <Menu size={22} />
        </button>

        {/* Breadcrumbs */}
        <div className="hidden sm:flex items-center text-sm font-medium text-slate-500">
          <Link to="/dashboard" className="hover:text-brand-600 transition-colors">Home</Link>
          {pathnames.map((name, index) => {
            const routeTo = `/${pathnames.slice(0, index + 1).join('/')}`;
            const isLast = index === pathnames.length - 1;
            const formattedName = name.charAt(0).toUpperCase() + name.slice(1);
            
            return (
              <React.Fragment key={name}>
                <ChevronRight size={14} className="mx-2 flex-shrink-0 text-slate-400" />
                {isLast ? (
                  <span className="text-slate-900 font-semibold">{formattedName}</span>
                ) : (
                  <Link to={routeTo} className="hover:text-brand-600 transition-colors">
                    {formattedName}
                  </Link>
                )}
              </React.Fragment>
            );
          })}
        </div>

        {/* Mobile: show current page name only */}
        <span className="sm:hidden text-sm font-semibold text-slate-900">
          {pathnames.length > 0
            ? pathnames[pathnames.length - 1].charAt(0).toUpperCase() + pathnames[pathnames.length - 1].slice(1)
            : 'Home'}
        </span>
      </div>

      <div className="flex items-center gap-2 sm:gap-4">
        {/* Search Bar (Hidden on small screens) */}
        <div className="hidden md:block relative w-64 mr-2">
          <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
            <Search size={16} className="text-slate-400" />
          </div>
          <input
            type="text"
            className="block w-full rounded-full border-0 bg-slate-100 py-1.5 pl-9 pr-4 text-sm text-slate-900 ring-1 ring-inset ring-transparent transition-all placeholder:text-slate-500 focus:bg-white focus:ring-2 focus:ring-inset focus:ring-brand-500"
            placeholder="Search..."
          />
        </div>

        {/* Mobile search icon */}
        <button className="md:hidden rounded-full p-2 text-slate-400 hover:bg-slate-100 hover:text-slate-600 transition-colors">
          <Search size={20} />
        </button>

        <button className="relative rounded-full p-2 text-slate-400 transition-colors hover:bg-slate-100 hover:text-slate-600 focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-2">
          <span className="absolute right-2 top-2 h-2 w-2 rounded-full bg-rose-500 ring-2 ring-white"></span>
          <Bell size={20} />
        </button>
        
        <div className="h-6 w-px bg-slate-200 hidden sm:block"></div>
        
        {/* Profile Dropdown */}
        <div className="relative" ref={profileRef}>
          <button 
            onClick={() => setIsProfileOpen(!isProfileOpen)}
            className="flex items-center gap-2 rounded-full focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-2"
          >
            <Avatar name={user?.name || 'User'} size="sm" />
          </button>

          {isProfileOpen && (
            <div className="absolute right-0 mt-2 w-48 origin-top-right rounded-xl bg-white py-1 shadow-lg shadow-slate-200/50 ring-1 ring-slate-200 focus:outline-none animate-in fade-in slide-in-from-top-2 duration-200">
              <div className="px-4 py-2 border-b border-slate-100 sm:hidden">
                <p className="text-sm font-medium text-slate-900">{user?.name || 'Admin User'}</p>
                <p className="text-xs text-slate-500">{user?.email || 'admin@studio.com'}</p>
              </div>
              <Link
                to="/profile"
                className="flex items-center gap-2 px-4 py-2 text-sm text-slate-700 hover:bg-slate-50 transition-colors"
                onClick={() => setIsProfileOpen(false)}
              >
                <User size={16} className="text-slate-400" />
                Your Profile
              </Link>
              <Link
                to="/settings"
                className="flex items-center gap-2 px-4 py-2 text-sm text-slate-700 hover:bg-slate-50 transition-colors"
                onClick={() => setIsProfileOpen(false)}
              >
                <Settings size={16} className="text-slate-400" />
                Settings
              </Link>
              <div className="h-px bg-slate-100 my-1"></div>
              <button
                onClick={handleLogout}
                className="flex w-full items-center gap-2 px-4 py-2 text-left text-sm text-rose-600 hover:bg-rose-50 transition-colors"
              >
                <LogOut size={16} className="text-rose-500" />
                Sign out
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Navbar;
