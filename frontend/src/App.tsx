import React, { useState } from 'react';
import logo from './logo.svg';
import './App.scss';

import { myTheme } from './mantine.theme';
import { ColorScheme, ColorSchemeProvider, MantineProvider, useMantineTheme } from '@mantine/core';
import SearchPage from './pages/SearchPage';
import SearchProvider from './providers/SearchProvider';

function App() {
  const [colorScheme, setColorScheme] = useState<ColorScheme>('light');
  const toggleColorScheme = (value?: ColorScheme) => {
    console.log(colorScheme)
    setColorScheme((colorScheme === 'dark' ? 'light' : 'dark'))
  }

  return (
    <MantineProvider theme={myTheme} withNormalizeCSS withGlobalStyles >

      <ColorSchemeProvider toggleColorScheme={toggleColorScheme} colorScheme={'dark'}>
        <SearchProvider>
          <SearchPage />
        </SearchProvider></ColorSchemeProvider>
    </MantineProvider>
  )
}
export default App;
