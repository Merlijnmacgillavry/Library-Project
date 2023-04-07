import { Radio, Stack } from '@mantine/core'
import React, { useContext } from 'react'
import { SearchContext } from '../providers/SearchProvider'

export default function Modelbar() {

    const { models, currentModel, changeModel } = useContext(SearchContext)

    function capitalizeFirstLetter(str: string): string {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    return (
        <div className="modelBar">
            <Radio.Group

                name="favoriteFramework"
                label="Select the retrieval method to run"
                description="Ranking can be found at ..."
                onChange={(value) => changeModel(value)}
                value={currentModel}
            >
                <Stack mt={'md'}>
                    {models && models.map((model) => {
                        return <Radio value={model} key={model} label={capitalizeFirstLetter(model.toUpperCase())} checked={currentModel === model} />
                    })}
                </Stack>
            </Radio.Group>
        </div>
    )
}

