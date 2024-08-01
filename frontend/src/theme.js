import { createGlobalStyle } from 'styled-components';

export const theme = {
  colors: {
    primary: '#1a73e8',
    primaryDark: '#1557b0',
    background: '#f0f2f5',
    border: '#ddd',
    error: '#d93025',
  },
};

export const GlobalStyle = createGlobalStyle`
  body {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
      'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
      sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    background-color: ${props => props.theme.colors.background};
  }
`;