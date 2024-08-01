import React from 'react';
import styled from 'styled-components';
import Card from '../common/Card';

const StyledStatCard = styled(Card)`
  text-align: center;
  padding: 1.5rem;
  transition: transform ${props => props.theme.transitions.default}, box-shadow ${props => props.theme.transitions.default};
  cursor: pointer;

  &:hover {
    transform: translateY(-5px);
    box-shadow: ${props => props.theme.shadows.medium};
  }

  h2 {
    color: ${props => props.theme.colors.primary};
    margin-bottom: 0.5rem;
    font-size: 1.2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
  }

  p {
    font-size: 2rem;
    font-weight: bold;
    color: ${props => props.theme.colors.text};
  }
`;

const StatCard = ({ title, value, icon: Icon, onClick }) => (
  <StyledStatCard onClick={onClick}>
    <h2>{Icon && <Icon />} {title}</h2>
    <p>{value}</p>
  </StyledStatCard>
);

export default StatCard;