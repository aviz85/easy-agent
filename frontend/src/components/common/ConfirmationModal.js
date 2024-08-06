import React from 'react';
import styled from 'styled-components';
import Button from './Button';

const ModalOverlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
`;

const ModalContent = styled.div`
  background-color: ${props => props.theme.colors.surface};
  padding: ${props => props.theme.spacing.lg};
  border-radius: 8px;
  box-shadow: ${props => props.theme.shadows.medium};
  max-width: 400px;
  width: 100%;
`;

const Title = styled.h2`
  margin-bottom: ${props => props.theme.spacing.md};
  color: ${props => props.theme.colors.primary};
`;

const Message = styled.p`
  margin-bottom: ${props => props.theme.spacing.lg};
`;

const ButtonContainer = styled.div`
  display: flex;
  justify-content: flex-end;
  gap: ${props => props.theme.spacing.sm};
`;

const ConfirmationModal = ({ isOpen, onClose, onConfirm, title, message }) => {
  if (!isOpen) return null;

  return (
    <ModalOverlay>
      <ModalContent>
        <Title>{title}</Title>
        <Message>{message}</Message>
        <ButtonContainer>
          <Button onClick={onClose}>Cancel</Button>
          <Button onClick={onConfirm} style={{ backgroundColor: props => props.theme.colors.error }}>Confirm</Button>
        </ButtonContainer>
      </ModalContent>
    </ModalOverlay>
  );
};

export default ConfirmationModal;