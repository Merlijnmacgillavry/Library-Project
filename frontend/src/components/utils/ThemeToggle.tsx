import { useTheme } from '@emotion/react';
import { useMantineColorScheme, ActionIcon, Group, Switch, useMantineTheme } from '@mantine/core';
import { IconSun, IconMoonStars } from '@tabler/icons-react';

export function ThemeToggle() {
    const { colorScheme, toggleColorScheme } = useMantineColorScheme();
    const theme = useMantineTheme()
    return (
        <Group position="center" my="xl">
            <Switch
                checked={theme.colorScheme === 'dark'}
                onChange={() => toggleColorScheme()}
                size="lg"
                radius="xl"
                onLabel={<IconSun color={theme.white} size="1.25rem" stroke={1.5} />}
                offLabel={<IconMoonStars color={theme.colors.gray[6]} size="1.25rem" stroke={1.5} />}
            />
        </Group>
    );
}