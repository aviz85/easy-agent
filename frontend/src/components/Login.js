import React, { useState } from 'react';
import styled from 'styled-components';
import { useNavigate } from 'react-router-dom';
import { login } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import Button from './common/Button';
import Input from './common/Input';
import Card from './common/Card';

const LoginContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: calc(100vh - 60px);
  padding: ${props => props.theme.spacing.md};
`;

const LoginCard = styled(Card)`
  width: 100%;
  max-width: 400px;
`;

const Title = styled.h2`
  text-align: center;
  color: ${props => props.theme.colors.primary};
  margin-bottom: ${props => props.theme.spacing.lg};
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: ${props => props.theme.spacing.md};
`;

const ErrorMessage = styled.p`
  color: ${props => props.theme.colors.error};
  text-align: center;
  margin-top: ${props => props.theme.spacing.md};
`;

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { login: authLogin } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const data = await login(username, password);
      authLogin(data);
      navigate('/dashboard');
    } catch (err) {
      setError('Invalid username or password');
    }
  };

  return (
    <LoginContainer>
      <LoginCard>
        <Title>Login</Title>
        <Form onSubmit={handleSubmit}>
          <Input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <Input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <Button type="submit">Log In</Button>
        </Form>
        {error && <ErrorMessage>{error}</ErrorMessage>}
      </LoginCard>
    </LoginContainer>
  );
};

export default Login;