import { Card, Title, useMantineTheme, Text, Image, Group, Stack } from '@mantine/core'
import React from 'react'
import { SearchResultT } from './SearchResults'
import icon from '../assets/document-icon.png'
import { useNavigate } from 'react-router-dom'
import { useHover } from '@mantine/hooks'

export type SearchResultCard = React.PropsWithChildren<{ data?: SearchResultT }>



export default function SearchResultCard(props: SearchResultCard) {
    const theme = useMantineTheme()
    const { hovered, ref } = useHover()
    const { data } = props
    const navigate = useNavigate()

    function navigateToResult(uuid: string | undefined): void {
        console.log(uuid)
        navigate('/search/' + uuid)
    }

    return (
        <Card radius={'sm'} className='searchResultCard' ref={ref} style={{ outline: hovered ? `solid ${theme.colors.primary}` : '' }}>
            <div className='searchResultCard-container'>
                <Image style={{ maxHeight: '100px' }} src={icon} alt="" />
                <div className='content'>
                    <Title onClick={() => navigateToResult(data?.uuid)} order={5} color={theme.colors.primary[0]}>{data?.title}</Title>
                    <Text fz={'12px'} fw={'normal'} >{data?.author} (author)</Text>
                    <Text lineClamp={5}>{data?.abstract}</Text>
                    <Text>{data?.['publication type']}</Text>
                </div>
            </div>
        </Card>
    )
}
