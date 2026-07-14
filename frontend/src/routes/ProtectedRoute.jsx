import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { hasPermission } from '../../utils/permissions';

const ProtectedRoute = ({ permission }) => {
    const { isAuthenticated, loading, user } = useAuth();

    if (loading) return null;

    if (!isAuthenticated) {
        return <Navigate to="/login" replace />;
    }

    if (permission && !hasPermission(user, permission)) {
        return <Navigate to="/403" replace />;
    }

    return <Outlet />;
};

export default ProtectedRoute;