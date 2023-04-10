import { AppShell, Aside, Col, Grid, Header, Input, MediaQuery, Navbar, Select, useMantineTheme, Text, Footer, Burger, Image, Box, TextInput, Stack, Button, Radio, Group, Center, Pagination, Switch, Title, useMantineColorScheme } from '@mantine/core';
import React, { useContext, useEffect, useState } from 'react'
import { myTheme } from '../mantine.theme';
import logo from '../assets/logo_tudelft.png';
import SearchBar from '../components/SearchBar';
import SearchResults, { SearchResultT } from '../components/SearchResults';
import Sidebar from '../components/Sidebar';
import Modelbar from '../components/Modelbar';
import StickyComponent from '../components/utils/StickyComponent';
import { SearchContext } from '../providers/SearchProvider';
import { BrowserRouter, createBrowserRouter, createRoutesFromElements, Link, Route, RouterProvider, Routes, useLoaderData, useNavigate, useParams } from 'react-router-dom';
import history from '../components/utils/history';
import { ThemeToggle } from '../components/utils/ThemeToggle';

export default function SearchPage() {
    const colorScheme = useMantineColorScheme()
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
                    <Modelbar />
                </Navbar>
            }
            aside={
                <MediaQuery smallerThan="sm" styles={{ display: 'none' }}>
                    <Aside p="md" hiddenBreakpoint="sm" width={{ sm: 200, lg: 300 }}>
                        <Sidebar />
                    </Aside>
                </MediaQuery>
            }
            header={
                <Header height={{ base: 50, md: 80 }} p="md" className={"header"}  >
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
                        <Group style={{ display: 'flex', justifyContent: 'space-between' }}>
                            <div></div>
                            <a href='/'><Image height='80' mx="auto" fit='contain' radius="md" src={logo} alt="Random image" /></a>
                            <ThemeToggle />
                        </Group>

                    </div>
                </Header>
            }
        >
            <BrowserRouter>
                <Routes>
                    <Route path='/' element={<SearchComponent />} />
                    <Route path='/search/:uuid' element={<SearchResult />} />
                </Routes></BrowserRouter>

        </AppShell >
    )
}
function SearchResult() {
    const theme = useMantineTheme()
    const navigate = useNavigate()
    let { uuid } = useParams()
    const { getDocument: getProfile } = useContext(SearchContext)
    const [result, setResult] = useState<SearchResultT | null>(null)

    useEffect(() => {
        let p = null
        if (uuid) {
            p = getProfile(uuid)
        }
        if (p) {
            setResult(p)
        } else {
            navigate("/")
        }
    }, [])

    return (
        <>
            {result && <Stack>
                <Title color={theme.colors.primary[0]}>{result.title}</Title>
                <Text size={'1em'} weight={'bold'}>Author</Text>
                <Text size={'0.75em'}>{result.author}</Text>
            </Stack>}</>
    )
}

function SearchComponent() {
    const { currentPage, changePage, lastQuery } = useContext(SearchContext)
    const theme = useMantineTheme()
    return (
        <StickyComponent>
            <div className='stickyContainer' style={{

                background: theme.colorScheme === 'dark' ? theme.colors.dark[8] : theme.colors.gray[0],

            }}>
                <Stack >
                    <SearchBar />
                    {lastQuery !== "" && <Center><Pagination value={currentPage} onChange={changePage} total={10} /></Center>}
                </Stack>
            </div>
            <SearchResults />
        </StickyComponent>
    )
}
