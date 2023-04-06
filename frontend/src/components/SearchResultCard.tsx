import { Card, Title, useMantineTheme, Text, Image, Group, Stack } from '@mantine/core'
import React from 'react'
import { SearchResultT } from './SearchResults'
import icon from '../assets/document-icon.png'
export type SearchResultCard = React.PropsWithChildren<{ data?: SearchResultT }>

export default function SearchResultCard(props: SearchResultCard) {
    const theme = useMantineTheme()
    const { data } = props
    return (
        <Card className='searchResultCard'>
            <div className='searchResultCard-container'>
                <img style={{ maxHeight: '100px' }} src={icon} alt="" />
                <div className='content'>
                    <Title order={5} color={theme.colors.primary[0]}>{data?.title}</Title>
                    <Text fz={'12px'} fw={'normal'} >{data?.author} (author)</Text>
                    <Text lineClamp={3}>{data?.abstract}</Text>
                    <Text>{data?.['publication type']}</Text>
                </div>
            </div>
        </Card>
    )
}
