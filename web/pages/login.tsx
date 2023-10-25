import getLayout from '@/components/layouts/main';
import { Button, Card, CardBody, Container, Flex, Heading, Text } from '@chakra-ui/react';
import { AiFillGithub } from 'react-icons/ai';

const Login = () => {
  return (
    <>
      <Flex minH={'calc(100vh - 64px)'}>
        <Container mx='auto' my='40' maxW='sm'>
          <Card>
            <CardBody>
              <Flex direction='column'>
                <Heading as='h1' fontSize='2xl' textAlign='center'>
                  ログイン
                </Heading>
                <Text py='2'>このサービスを利用するには、Github連携が必要です。</Text>
                <Button leftIcon={<AiFillGithub size='26px' />} bgColor='#171515' size='lg'>
                  Login with Github
                </Button>
              </Flex>
            </CardBody>
          </Card>
        </Container>
      </Flex>
    </>
  );
};

Login.getLayout = getLayout;

export default Login;
