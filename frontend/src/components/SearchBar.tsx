import { Box, Button, Group, TextInput } from '@mantine/core';
import { useForm } from '@mantine/form';
import React from 'react'

export default function SearchBar() {
    const form = useForm({
        initialValues: {
            query: '',
        },

        validate: {
            query: (query) => (query === '' ? 'Must not be empty!' : null),
        },
    });

    function search(query: string) {
        fetch('http://localhost:5000/search?' + new URLSearchParams({
            query: query,
            page: '1'
        })).then((response) => {
            response.json().then((value) => {
                console.log(value)
            })
        })
    }

    return (
        <form onSubmit={form.onSubmit((values) => search(values.query))} style={{ width: '100%' }}>
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
