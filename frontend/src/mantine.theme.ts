import { MantineThemeOverride } from "@mantine/core";

export const myTheme: MantineThemeOverride = {
    colorScheme: 'dark',

    colors: {
        brand: [
            "#83BCC6",
            "#65B7C7",
            "#43B7CD",
            "#22B9D6",
            "#0AB6D7",
            "#1B97AF",
            "#267F90",
            "#2C6C78",
            "#2E5C65",
            "#2F5056",
        ],
        primary: ["#00B5D8"],
        secondary: ["#00A7F4"],
        success: ["#157347"],
        info: ["#31d2f2"],
        warning: ["#ffca2c"],
        danger: ["#dc3545"]
    },
    primaryColor: "brand",
    fontFamily: "Open sans",
    fontSizes: {
        xs: "13",
        sm: "14",
        md: "15",
        lg: "17",
        xl: "19"
    },
    lineHeight: "19px",
    headings: {
        fontFamily: "Open sans",
        fontWeight: 500,
        sizes: {
            h1: { fontSize: "38px", lineHeight: "48px" },
            h2: { fontSize: "30px", lineHeight: "40px" },
            h3: { fontSize: "22px", lineHeight: "26px" },
            h4: { fontSize: "17px", lineHeight: "24px" },
            h5: { fontSize: "15px", lineHeight: "20px" }
        }
    },
    defaultRadius: 'md',
    radius: {
        xs: "0",
        sm: "0",
        md: "15",
        lg: "0",
        xl: "0"
    },
    other: {
        defaultText: {
            desktop: "lg",
            mobile: "sm"
        },
        lineHeights: {
            xs: "14px",
            sm: "15px",
            md: "17px",
            lg: "19px",
            xl: "22px"
        }
    }
};
