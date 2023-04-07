import { Stack, Title, Text, useMantineTheme } from '@mantine/core'
import React from 'react'

export default function Sidebar() {
    const theme = useMantineTheme()

    return (
        <Stack className={"sidebar"} spacing={'lg'}>
            <div className='sidebar-filter'>
                <Title order={4}>Collection</Title>
                <Stack>
                    <Text color={theme.colors.primary[0]} fz={'0.85em'} className={"filterChoice"}>Student theses (4789)</Text>
                </Stack>

            </div>
            <div className='sidebar-filter'>
                <Title order={4}>Collection</Title>
                <Stack>
                    <Text color={theme.colors.primary[0]} fz={'0.85em'} className={"filterChoice"}>Student theses (4789)</Text>
                </Stack>

            </div>
        </Stack>
    )
}

export type filterT = {
    name: string,
    options: filterOptionT
}
export type filterOptionT = {
    text: string,
    count: number,
    active: false
}


