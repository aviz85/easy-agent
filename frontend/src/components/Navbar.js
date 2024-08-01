import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import styled from 'styled-components';
import { useAuth } from '../contexts/AuthContext';

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

const NavLinks = styled.div`
  display: flex;
  align-items: center;

  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    display: ${props => props.isOpen ? 'flex' : 'none'};
    flex-direction: column;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background-color: ${props => props.theme.colors.surface};
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    padding: 1rem;
  }
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
    text-decoration: none;  // Explicitly remove text decoration on hover
  }

  &:focus {
    outline: none;
    text-decoration: none;  // Remove text decoration on focus as well
  }

  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    margin: 0.5rem 0;
    width: 100%;
    text-align: center;
  }
`;

const NavButton = styled.button`
  background-color: transparent;
  color: ${props => props.theme.colors.primary};
  border: 2px solid ${props => props.theme.colors.primary};
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
  font-weight: bold;

  &:hover {
    background-color: ${props => props.theme.colors.primary};
    color: ${props => props.theme.colors.surface};
  }

  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    width: 100%;
    margin-top: 0.5rem;
  }
`;

const MenuToggle = styled.button`
  display: none;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: ${props => props.theme.colors.primary};

  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    display: block;
  }
`;

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  return (
    <NavContainer>
      <NavContent>
        <Logo to="/">EasyAgent</Logo>
        <MenuToggle onClick={toggleMenu}>
          {isOpen ? '✕' : '☰'}
        </MenuToggle>
        <NavLinks isOpen={isOpen}>
          {user ? (
            <>
              <NavLink to="/dashboard" className={location.pathname === '/dashboard' ? 'active' : ''}>Dashboard</NavLink>
              <NavLink to="/profile" className={location.pathname === '/profile' ? 'active' : ''}>Profile</NavLink>
              <NavLink to="/create-agreement" className={location.pathname === '/create-agreement' ? 'active' : ''}>Create Agreement</NavLink>
              <NavButton onClick={handleLogout}>Logout</NavButton>
            </>
          ) : (
            <>
              <NavLink to="/login" className={location.pathname === '/login' ? 'active' : ''}>Login</NavLink>
              <NavLink to="/register" className={location.pathname === '/register' ? 'active' : ''}>Register</NavLink>
            </>
          )}
        </NavLinks>
      </NavContent>
    </NavContainer>
  );
};

export default Navbar;