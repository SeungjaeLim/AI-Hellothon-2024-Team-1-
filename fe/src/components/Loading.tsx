import { Flex, Spin } from "antd";

import { LoadingOutlined } from "@ant-design/icons";

interface LoadingProps {
  size?: "small" | "default" | "large";
}

function Loading({ size = "default" }: LoadingProps) {
  return (
    <Flex
      align="center"
      gap="middle"
      className="flex h-full w-full items-center justify-center"
    >
      <Spin indicator={<LoadingOutlined spin />} size={size} />
    </Flex>
  );
}

export default Loading;
