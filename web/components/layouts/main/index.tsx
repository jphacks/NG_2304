import React, { ReactElement } from 'react';
import Header from '@/components/layouts/main/Header';

type LayoutProps = Required<{
  readonly children: ReactElement;
}>;

export const Layout = ({ children }: LayoutProps) => (
  <>
    <Header />
    <div>{children}</div>
  </>
);
const getLayout = (page: React.ReactElement) => <Layout>{page}</Layout>;

export default getLayout;
