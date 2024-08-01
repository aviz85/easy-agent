import { createGlobalStyle } from 'styled-components';

export const theme = {
  colors: {
    primary: '#1a73e8',
    primaryLight: '#4285f4',
    primaryDark: '#1557b0',
    secondary: '#34a853',
    background: '#f8f9fa',
    surface: '#ffffff',
    text: '#202124',
    textLight: '#5f6368',
    border: '#dadce0',
    error: '#d93025',
    success: '#0f9d58',
  },
  fonts: {
    main: "'Roboto', sans-serif",
  },
  breakpoints: {
    mobile: '768px',
  },
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px',
  },
  shadows: {
    small: '0 1px 2px 0 rgba(60,64,67,0.3), 0 1px 3px 1px rgba(60,64,67,0.15)',
    medium: '0 4px 6px 0 rgba(60,64,67,0.3), 0 2px 4px 0 rgba(60,64,67,0.15)',
    large: '0 10px 20px 0 rgba(60,64,67,0.3), 0 6px 6px 0 rgba(60,64,67,0.15)',
  },
  transitions: {
    default: '0.3s ease',
  },
};

export const GlobalStyle = createGlobalStyle`
  body {
    margin: 0;
    padding: 0;
    font-family: ${props => props.theme.fonts.main};
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    background-color: ${props => props.theme.colors.background};
    color: ${props => props.theme.colors.text};
  }

  a {
    text-decoration: none;
  }

  * {
    box-sizing: border-box;
  }

  h1, h2, h3, h4, h5, h6 {
    margin: 0;
    font-weight: 500;
  }

  a {
    color: ${props => props.theme.colors.primary};
    text-decoration: none;
    &:hover {
      text-decoration: underline;
    }
  }
`;