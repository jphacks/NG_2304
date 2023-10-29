import { Box, Flex, Container, Heading, useColorModeValue } from '@chakra-ui/react';
import Link from 'next/link';

const Header = () => {
  return (
    <>
      <Box w='100%' bg={useColorModeValue('gray.100', 'gray.900')} px={4}>
        <Container maxW='1200px'>
          <Flex h='64px' justifyContent='space-between' alignItems='center'>
            <Link href='/' passHref>
              <Heading as='h1' fontSize='2xl' cursor='pointer'>
                Bithealth
              </Heading>
            </Link>
            <Flex py='4' justifyContent='right' alignItems='center'>
              <p>Test</p>
              <p>Test</p>
            </Flex>
          </Flex>
        </Container>
      </Box>
    </>
  );
};

export default Header;
