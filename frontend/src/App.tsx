import React from 'react';
import logo from './logo.svg';
import './App.css';

import { myTheme } from './mantine.theme';
import { MantineProvider, useMantineTheme } from '@mantine/core';
import SearchPage from './pages/SearchPage';
import SearchProvider from './providers/SearchProvider';

function App() {
  return (
    <MantineProvider theme={myTheme} withNormalizeCSS withGlobalStyles >

      <SearchProvider>
        <SearchPage />
      </SearchProvider>
    </MantineProvider>
  )
}
export default App;
