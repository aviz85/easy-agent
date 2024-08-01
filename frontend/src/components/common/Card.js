import styled from 'styled-components';

const Card = styled.div`
  background-color: ${props => props.theme.colors.surface};
  border-radius: 8px;
  padding: ${props => props.theme.spacing.lg};
  box-shadow: ${props => props.theme.shadows.medium};
`;

export default Card;