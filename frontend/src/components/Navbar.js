import React, { useState, useEffect, useRef } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import styled from 'styled-components';
import { useAuth } from '../contexts/AuthContext';
import { FaBell, FaUser, FaChevronDown } from 'react-icons/fa';

const NavContainer = styled.nav`
  background-color: ${props => props.theme.colors.surface};
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1rem 2rem;
  position: sticky;
  top: 0;
  z-index: 1000;
`;

const NavContent = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
`;

const Logo = styled(Link)`
  font-size: 1.5rem;
  font-weight: bold;
  color: ${props => props.theme.colors.primary};
  text-decoration: none;
`;

const NavLinksLeft = styled.div`
  display: flex;
  align-items: center;
  margin-right: auto;
  margin-left: 2rem;
`;

const NavLinksRight = styled.div`
  display: flex;
  align-items: center;
`;

const NavLink = styled(Link)`
  color: ${props => props.theme.colors.text};
  text-decoration: none;
  padding: 0.5rem 1rem;
  margin: 0 0.5rem;
  border-radius: 4px;
  transition: background-color 0.3s, color 0.3s;

  &:hover, &.active {
    background-color: ${props => props.theme.colors.primaryLight};
    color: ${props => props.theme.colors.surface};
  }
`;

const NavButton = styled.button`
  background-color: transparent;
  color: ${props => props.theme.colors.primary};
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  font-size: 1rem;
`;

const NotificationIcon = styled.div`
  position: relative;
  cursor: pointer;
  margin-right: 1rem;
  transition: transform 0.3s ease;

  &:hover {
    transform: scale(1.1);
  }
`;

const NotificationBadge = styled.span`
  position: absolute;
  top: -5px;
  right: -5px;
  background-color: ${props => props.theme.colors.error};
  color: ${props => props.theme.colors.surface};
  border-radius: 50%;
  padding: 2px 5px;
  font-size: 0.7rem;
  transition: all 0.3s ease;

  ${NotificationIcon}:hover & {
    transform: scale(1.1);
    box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
  }
`;

const NotificationPopup = styled.div`
  position: absolute;
  top: 100%;
  right: -10px;
  background-color: ${props => props.theme.colors.surface};
  border-radius: 4px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 1rem;
  min-width: 200px;
  z-index: 1000;
  opacity: ${props => props.isVisible ? 1 : 0};
  transform: ${props => props.isVisible ? 'translateY(0)' : 'translateY(-10px)'};
  transition: opacity 0.3s ease, transform 0.3s ease;
`;

const NotificationItem = styled.div`
  padding: 0.5rem 0;
  border-bottom: 1px solid ${props => props.theme.colors.border};
  
  &:last-child {
    border-bottom: none;
  }
`;

const ProfileDropdown = styled.div`
  position: relative;
`;

const DropdownContent = styled.div`
  display: ${props => props.isOpen ? 'block' : 'none'};
  position: absolute;
  right: 0;
  top: 100%;
  background-color: ${props => props.theme.colors.surface};
  min-width: 180px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  border-radius: 4px;
  overflow: hidden;
  z-index: 1;
`;

const DropdownItem = styled(Link)`
  color: ${props => props.theme.colors.text};
  padding: 12px 16px;
  text-decoration: none;
  display: block;
  transition: background-color 0.3s;

  &:hover {
    background-color: ${props => props.theme.colors.primaryLight};
    color: ${props => props.theme.colors.surface};
  }
`;

const Navbar = () => {
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [notificationCount, setNotificationCount] = useState(3);
  const dropdownRef = useRef(null);
  const [isNotificationOpen, setIsNotificationOpen] = useState(false);
  const notificationRef = useRef(null);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleNotificationClick = () => {
    setIsNotificationOpen(!isNotificationOpen);
  };

  const toggleProfileDropdown = () => {
    setIsProfileOpen(!isProfileOpen);
  };

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsProfileOpen(false);
      }
      if (notificationRef.current && !notificationRef.current.contains(event.target)) {
        setIsNotificationOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  return (
    <NavContainer>
      <NavContent>
        <Logo to="/">EasyAgent</Logo>
        {user && (
          <>
            <NavLinksLeft>
              <NavLink to="/dashboard" className={location.pathname === '/dashboard' ? 'active' : ''}>Dashboard</NavLink>
              <NavLink to="/agreements" className={location.pathname === '/agreements' ? 'active' : ''}>Agreements</NavLink>
              <NavLink to="/clients" className={location.pathname === '/clients' ? 'active' : ''}>Clients</NavLink>
            </NavLinksLeft>
            <NavLinksRight>
              <NotificationIcon onClick={handleNotificationClick} ref={notificationRef}>
                <FaBell size={20} />
                {notificationCount > 0 && (
                  <NotificationBadge>{notificationCount}</NotificationBadge>
                )}
                <NotificationPopup isVisible={isNotificationOpen}>
                  <NotificationItem>New message from John</NotificationItem>
                  <NotificationItem>Your agreement was approved</NotificationItem>
                  <NotificationItem>New client signed up</NotificationItem>
                </NotificationPopup>
              </NotificationIcon>
              <ProfileDropdown ref={dropdownRef}>
                <NavButton onClick={toggleProfileDropdown}>
                  <FaUser size={16} style={{ marginRight: '5px' }} />
                  {user.name || 'Profile'}
                  <FaChevronDown size={12} style={{ marginLeft: '5px' }} />
                </NavButton>
                <DropdownContent isOpen={isProfileOpen}>
                  <DropdownItem to="/profile">Profile</DropdownItem>
                  <DropdownItem as="button" onClick={handleLogout}>Logout</DropdownItem>
                </DropdownContent>
              </ProfileDropdown>
            </NavLinksRight>
          </>
        )}
        {!user && (
          <NavLinksRight>
            <NavLink to="/login" className={location.pathname === '/login' ? 'active' : ''}>Login</NavLink>
            <NavLink to="/register" className={location.pathname === '/register' ? 'active' : ''}>Register</NavLink>
          </NavLinksRight>
        )}
      </NavContent>
    </NavContainer>
  );
};

export default Navbar;