import React from 'react';
import logo from './logo.svg';
import './App.css';

import { myTheme } from './mantine.theme';
import { MantineProvider, useMantineTheme } from '@mantine/core';
import SearchPage from './pages/SearchPage';

function App() {
  return (
    <MantineProvider theme={myTheme} withNormalizeCSS withGlobalStyles >

      <div className="main">
        <SearchPage />
      </div>
    </MantineProvider>
  )
}
export default App;
