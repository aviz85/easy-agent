import styled from 'styled-components';

const Button = styled.button`
  background-color: ${props => props.theme.colors.primary};
  color: white;
  border: none;
  border-radius: 4px;
  padding: ${props => props.theme.spacing.sm} ${props => props.theme.spacing.md};
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s, box-shadow 0.3s;

  &:hover {
    background-color: ${props => props.theme.colors.primaryDark};
    box-shadow: ${props => props.theme.shadows.small};
  }

  &:disabled {
    background-color: ${props => props.theme.colors.border};
    cursor: not-allowed;
  }
`;

export default Button;