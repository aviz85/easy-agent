import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import { useAuth } from '../contexts/AuthContext';
import Button from './common/Button';

const Nav = styled.nav`
  background-color: ${props => props.theme.colors.primary};
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const Logo = styled(Link)`
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
`;

const NavItems = styled.div`
  display: flex;
  align-items: center;

  @media (max-width: 768px) {
    display: ${({ isOpen }) => (isOpen ? 'flex' : 'none')};
    flex-direction: column;
    position: absolute;
    top: 70px;
    left: 0;
    right: 0;
    background-color: ${props => props.theme.colors.primary};
    padding: 1rem;
  }
`;

const NavLink = styled(Link)`
  color: white;
  text-decoration: none;
  margin-left: 1.5rem;
  transition: opacity 0.3s;

  &:hover {
    opacity: 0.8;
  }

  @media (max-width: 768px) {
    margin: 0.5rem 0;
  }
`;

const NavButton = styled(Button)`
  margin-left: 1.5rem;
  background-color: white;
  color: ${props => props.theme.colors.primary};

  &:hover {
    background-color: ${props => props.theme.colors.background};
  }

  @media (max-width: 768px) {
    margin: 0.5rem 0;
    width: 100%;
  }
`;

const Hamburger = styled.div`
  display: none;
  flex-direction: column;
  cursor: pointer;

  span {
    height: 2px;
    width: 25px;
    background-color: white;
    margin-bottom: 4px;
    border-radius: 5px;
  }

  @media (max-width: 768px) {
    display: flex;
  }
`;

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <Nav>
      <Logo to="/">EasyAgent</Logo>
      <Hamburger onClick={() => setIsOpen(!isOpen)}>
        <span></span>
        <span></span>
        <span></span>
      </Hamburger>
      <NavItems isOpen={isOpen}>
        {user ? (
          <>
            <NavLink to="/dashboard">Dashboard</NavLink>
            <NavLink to="/profile">Profile</NavLink>
            <NavLink to="/create-agreement">Create Agreement</NavLink>
            <NavButton onClick={handleLogout}>Logout</NavButton>
          </>
        ) : (
          <>
            <NavLink to="/login">Login</NavLink>
            <NavLink to="/register">Register</NavLink>
          </>
        )}
      </NavItems>
    </Nav>
  );
};

export default Navbar;