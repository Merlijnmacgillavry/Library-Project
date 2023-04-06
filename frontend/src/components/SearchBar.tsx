import { Box, Button, Group, TextInput } from '@mantine/core';
import { useForm } from '@mantine/form';
import React, { useContext } from 'react'
import { SearchContext } from '../providers/SearchProvider';

export default function SearchBar() {
    const { search } = useContext(SearchContext)
    const form = useForm({
        initialValues: {
            query: '',
        },

        validate: {
            query: (query) => (query === '' ? 'Must not be empty!' : null),
        },
    });
    function executeQuery(query: string){
        search(query)
    }


    return (
        <form onSubmit={form.onSubmit((values) => executeQuery(values.query))} style={{ width: '100%' }}>
            <Group w={'100%'} align='end' mt="md" noWrap >
                <TextInput

                    withAsterisk
                    label=""
                    placeholder="How does information retrieval work?"
                    w={'100%'}
                    {...form.getInputProps('query')}
                />
                <Button type="submit">Search</Button>

            </Group >
        </form>
    )
}
