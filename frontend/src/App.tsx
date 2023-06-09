import React, { useState } from 'react';
import logo from './logo.svg';
import './App.scss';

import { myTheme } from './mantine.theme';
import { ColorScheme, ColorSchemeProvider, MantineProvider, useMantineTheme } from '@mantine/core';
import SearchPage from './pages/SearchPage';
import SearchProvider from './providers/SearchProvider';

function App() {
  const [colorScheme, setColorScheme] = useState<ColorScheme>('dark');
  const toggleColorScheme = (value?: ColorScheme) => {
    setColorScheme((colorScheme === 'dark' ? 'light' : 'dark'))
  }

  return (
    <MantineProvider theme={{ ...myTheme, colorScheme: colorScheme }} withNormalizeCSS withGlobalStyles >
      <ColorSchemeProvider toggleColorScheme={toggleColorScheme} colorScheme={'dark'}>
        <SearchProvider>
          <SearchPage />
        </SearchProvider></ColorSchemeProvider>
    </MantineProvider>
  )
}
export default App;
