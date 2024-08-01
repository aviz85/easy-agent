import React from 'react';
import styled from 'styled-components';
import Card from '../common/Card';

const ActionsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
`;

const ActionButton = styled.button`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: ${props => props.theme.colors.surface};
  color: ${props => props.theme.colors.primary};
  border: none;
  border-radius: 8px;
  padding: 1rem;
  cursor: pointer;
  transition: all ${props => props.theme.transitions.default};
  box-shadow: ${props => props.theme.shadows.small};

  &:hover {
    background-color: ${props => props.theme.colors.primary};
    color: ${props => props.theme.colors.surface};
    transform: translateY(-2px);
    box-shadow: ${props => props.theme.shadows.medium};
  }

  svg {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
  }

  span {
    font-size: 0.8rem;
    text-align: center;
  }
`;

const QuickActions = ({ actions }) => (
  <Card>
    <h2>Quick Actions</h2>
    <ActionsGrid>
      {actions.map((action, index) => (
        <ActionButton key={index} onClick={action.action}>
          <action.icon />
          <span>{action.title}</span>
        </ActionButton>
      ))}
    </ActionsGrid>
  </Card>
);

export default QuickActions;