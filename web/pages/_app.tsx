import '@/styles/globals.css';
import type { AppProps } from 'next/app';
import { extendTheme } from '@chakra-ui/react';
import { ChakraProvider } from '@chakra-ui/react';
import { NextPage } from 'next';
import { Work_Sans, Inter } from 'next/font/google';

const work = Work_Sans({
  variable: '--font-work-sans',
  weight: ['700'],
  subsets: ['latin'],
});

const inter = Inter({
  variable: '--font-inter',
  weight: ['400', '500', '600'],
  subsets: ['latin'],
});

export const theme = extendTheme({
  initialColorMode: 'system',
  useSystemColorMode: true,
  fonts: {
    body: inter.style.fontFamily,
    heading: work.style.fontFamily,
  },
});

type NextPageWithLayout = NextPage & {
  getLayout?: (page: React.ReactElement) => React.ReactNode;
};

type AppPropsWithLayout = AppProps & {
  Component: NextPageWithLayout;
};

export default function App({ Component, pageProps }: AppPropsWithLayout) {
  const getLayout = Component.getLayout ?? ((page) => page);

  return <ChakraProvider theme={theme}>{getLayout(<Component {...pageProps} />)}</ChakraProvider>;
}
