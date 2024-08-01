import styled from 'styled-components';

const Input = styled.input`
  width: 100%;
  padding: ${props => props.theme.spacing.sm};
  border: 1px solid ${props => props.theme.colors.border};
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.3s, box-shadow 0.3s;

  &:focus {
    outline: none;
    border-color: ${props => props.theme.colors.primary};
    box-shadow: 0 0 0 2px ${props => props.theme.colors.primaryLight}40;
  }
`;

export default Input;