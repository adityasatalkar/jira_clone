import styled from 'styled-components';

import { color, font } from 'shared/utils/styles';
import { Button } from 'shared/components';

export const DetailsSurface = styled.div`
  margin-top: 16px;
  border: 1px solid ${color.borderLightest};
  border-radius: 4px;
  background: #fff;
`;

export const DetailsTop = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  min-height: 64px;
  padding: 14px 18px;
  border-bottom: 1px solid ${color.borderLightest};
  @media (max-width: 1100px) {
    row-gap: 10px;
  }
`;

export const DetailsTopLeft = styled.div`
  display: flex;
  align-items: center;
`;

export const BackButton = styled(Button)`
  margin-right: 8px;
`;

export const IssueKey = styled.div`
  color: ${color.textMedium};
  letter-spacing: 0.3px;
  ${font.bold}
  ${font.size(12.5)}
`;

export const DetailsTopRight = styled.div`
  display: flex;
  align-items: center;
  & > * {
    margin-left: 6px;
  }
`;

export const DetailsContent = styled.div`
  display: flex;
  @media (max-width: 1200px) {
    display: block;
  }
`;

export const DetailsMain = styled.div`
  width: calc(100% - 360px);
  min-width: 0;
  padding: 0 28px 36px;
  @media (max-width: 1200px) {
    width: 100%;
  }
`;

export const CommentsBlock = styled.div`
  margin-top: 10px;
`;

export const DetailsSidebar = styled.aside`
  width: 360px;
  border-left: 1px solid ${color.borderLightest};
  background: ${color.backgroundLightest};
  @media (max-width: 1200px) {
    width: 100%;
    border-top: 1px solid ${color.borderLightest};
    border-left: none;
  }
`;

export const SidebarCard = styled.div`
  padding: 20px 16px 24px;
`;
