import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import api from '../services/api';
import Button from './common/Button';
import Input from './common/Input';

const ProfileContainer = styled.div`
  padding: 2rem;
`;

const Title = styled.h1`
  color: ${props => props.theme.colors.primary};
  margin-bottom: 1rem;
`;

const Form = styled.form`
  max-width: 400px;
`;

const Profile = () => {
  const [profile, setProfile] = useState({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
  });

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await api.get('/profile/');
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
      await api.put('/profile/', profile);
      alert('Profile updated successfully');
    } catch (error) {
      console.error('Error updating profile:', error);
      alert('Failed to update profile');
    }
  };

  return (
    <ProfileContainer>
      <Title>Profile</Title>
      <Form onSubmit={handleSubmit}>
        <Input
          type="text"
          name="username"
          value={profile.username}
          onChange={handleChange}
          placeholder="Username"
          disabled
        />
        <Input
          type="email"
          name="email"
          value={profile.email}
          onChange={handleChange}
          placeholder="Email"
        />
        <Input
          type="text"
          name="first_name"
          value={profile.first_name}
          onChange={handleChange}
          placeholder="First Name"
        />
        <Input
          type="text"
          name="last_name"
          value={profile.last_name}
          onChange={handleChange}
          placeholder="Last Name"
        />
        <Button type="submit">Update Profile</Button>
      </Form>
    </ProfileContainer>
  );
};

export default Profile;