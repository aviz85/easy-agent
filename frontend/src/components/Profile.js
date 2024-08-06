import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { getProfile, updateProfile } from '../services/api';
import Button from './common/Button';
import Input from './common/Input';
import Card from './common/Card';

const ProfileContainer = styled.div`
  padding: ${props => props.theme.spacing.lg};
  max-width: 800px;
  margin: 0 auto;
`;

const Title = styled.h1`
  color: ${props => props.theme.colors.primary};
  margin-bottom: ${props => props.theme.spacing.lg};
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: ${props => props.theme.spacing.md};
`;

const FieldGroup = styled.div`
  display: flex;
  flex-direction: column;
`;

const Label = styled.label`
  font-weight: 500;
  margin-bottom: ${props => props.theme.spacing.xs};
  color: ${props => props.theme.colors.textLight};
`;

const SuccessMessage = styled.p`
  color: ${props => props.theme.colors.success};
  text-align: center;
  margin-top: ${props => props.theme.spacing.md};
`;

const Profile = () => {
  const [profile, setProfile] = useState({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
  });
  const [successMessage, setSuccessMessage] = useState('');

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await getProfile();
        setProfile(response.data);
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    };

    fetchProfile();
  }, []);

  const handleChange = (e) => {
    setProfile({ ...profile, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await updateProfile(profile);
      setSuccessMessage('Profile updated successfully');
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (error) {
      console.error('Error updating profile:', error);
    }
  };

  return (
    <ProfileContainer>
      <Title>Profile</Title>
      <Card>
        <Form onSubmit={handleSubmit}>
          <FieldGroup>
            <Label htmlFor="username">Username</Label>
            <Input
              id="username"
              type="text"
              name="username"
              value={profile.username}
              onChange={handleChange}
              disabled
            />
          </FieldGroup>
          <FieldGroup>
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              name="email"
              value={profile.email}
              onChange={handleChange}
            />
          </FieldGroup>
          <FieldGroup>
            <Label htmlFor="first_name">First Name</Label>
            <Input
              id="first_name"
              type="text"
              name="first_name"
              value={profile.first_name}
              onChange={handleChange}
            />
          </FieldGroup>
          <FieldGroup>
            <Label htmlFor="last_name">Last Name</Label>
            <Input
              id="last_name"
              type="text"
              name="last_name"
              value={profile.last_name}
              onChange={handleChange}
            />
          </FieldGroup>
          <Button type="submit">Update Profile</Button>
        </Form>
        {successMessage && <SuccessMessage>{successMessage}</SuccessMessage>}
      </Card>
    </ProfileContainer>
  );
};

export default Profile;