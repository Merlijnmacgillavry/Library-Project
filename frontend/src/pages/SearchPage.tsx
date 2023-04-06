import { AppShell, Aside, Col, Grid, Header, Input, MediaQuery, Navbar, Select, useMantineTheme, Text, Footer, Burger, Image, Box, TextInput, Stack, Button } from '@mantine/core';
import React, { useState } from 'react'
import { myTheme } from '../mantine.theme';
import logo from '../assets/logo_tudelft.png';
import SearchBar from '../components/SearchBar';
import SearchResults from '../components/SearchResults';

export default function SearchPage() {
    const theme = useMantineTheme()

    const [opened, setOpened] = useState(false);

    // const filteredData = data.filter((item) => {
    //     if (selectedFilter && item.category !== selectedFilter) {
    //         return false;
    //     }
    //     if (searchTerm && !item.name.toLowerCase().includes(searchTerm.toLowerCase())) {
    //         return false;
    //     }
    //     return true;
    // });

    // const categories = Array.from(new Set(data.map((item) => item.category)));

    return (
        <AppShell
            styles={{
                main: {
                    background: theme.colorScheme === 'dark' ? theme.colors.dark[8] : theme.colors.gray[0],
                },
            }}
            navbarOffsetBreakpoint="sm"
            asideOffsetBreakpoint="sm"
            navbar={
                <Navbar p="md" hiddenBreakpoint="sm" hidden={!opened} width={{ sm: 200, lg: 300 }}>

                    <Text>Application navbar</Text>
                </Navbar>
            }
            aside={
                <MediaQuery smallerThan="sm" styles={{ display: 'none' }}>
                    <Aside p="md" hiddenBreakpoint="sm" width={{ sm: 200, lg: 300 }}>
                        <Text>Application sidebar</Text>
                    </Aside>
                </MediaQuery>
            }
            header={
                <Header height={{ base: 50, md: 80 }} p="md" style={{ backgroundColor: theme.colors.brand[4] }}  >
                    <div style={{ display: 'flex', alignItems: 'center', height: '100%' }}>
                        <MediaQuery largerThan="sm" styles={{ display: 'none' }}>
                            <Burger
                                opened={opened}
                                onClick={() => setOpened((o) => !o)}
                                size="sm"
                                color={theme.colors.gray[6]}
                                mr="xl"
                            />
                        </MediaQuery>
                        {/* <Image height='80' mx="auto" fit='contain' radius="md" src={logo} alt="Random image" /> */}
                        <Text color={theme.white}>TU Delft Library ++</Text>
                    </div>
                </Header>
            }
        >
            <Stack h={300} sx={(theme) => ({ backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[8] : theme.colors.gray[0] })}>
                <SearchBar />
                <SearchResults />
            </Stack>
        </AppShell >
    )
}

