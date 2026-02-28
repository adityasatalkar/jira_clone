import styled, { css } from 'styled-components';
import { Link } from 'react-router-dom';

import {
  color,
  font,
  mixin,
  issueStatusBackgroundColors,
  issueStatusColors,
} from 'shared/utils/styles';
import { Avatar, Button, Select } from 'shared/components';

export const ViewHeader = styled.div`
  margin-top: 8px;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
`;

export const HeaderTitles = styled.div``;

export const Heading = styled.h2`
  ${font.size(24)}
  ${font.medium}
`;

export const Subheading = styled.p`
  margin-top: 4px;
  color: ${color.textMedium};
  ${font.size(14)}
`;

export const Toolbar = styled.div`
  display: flex;
  align-items: center;
  margin-top: 18px;
  padding: 12px;
  border: 1px solid ${color.borderLightest};
  border-radius: 4px;
  background: #fff;
`;

export const SearchInput = styled.div`
  width: 230px;
  margin-right: 14px;
`;

export const AvatarFilters = styled.div`
  display: flex;
  flex-direction: row-reverse;
  margin-right: 12px;
`;

export const AvatarIsActiveBorder = styled.div`
  display: inline-flex;
  margin-left: -2px;
  border-radius: 50%;
  transition: transform 0.1s;
  ${mixin.clickable}
  ${props => props.isActive && `box-shadow: 0 0 0 3px ${color.primary}`}
  &:hover {
    transform: translateY(-3px);
  }
`;

export const ToolbarAvatar = styled(Avatar)`
  box-shadow: 0 0 0 2px #fff;
`;

export const ToolbarActions = styled.div`
  display: flex;
  align-items: center;
  flex-wrap: wrap;
`;

export const FilterButton = styled(Button)`
  margin: 4px 6px 4px 0;
`;

export const ClearAll = styled.div`
  margin-left: 6px;
  padding-left: 10px;
  border-left: 1px solid ${color.borderLightest};
  color: ${color.textDark};
  ${font.size(14)}
  ${mixin.clickable}
  &:hover {
    color: ${color.textMedium};
  }
`;

export const TableContainer = styled.div`
  margin-top: 16px;
  border: 1px solid ${color.borderLightest};
  border-radius: 4px;
  overflow-x: auto;
  overflow-y: visible;
  background: #fff;
`;

export const Table = styled.table`
  width: 100%;
  min-width: 1250px;
  border-collapse: collapse;
  table-layout: fixed;
`;

export const ColumnHeader = styled.th`
  text-align: left;
  padding: 10px 12px;
  border-bottom: 1px solid ${color.borderLightest};
  color: ${color.textDark};
  background: ${color.backgroundLightest};
  ${font.bold}
  ${font.size(12.5)}
  ${props => props.width && `width: ${props.width}px`}
`;

export const Cell = styled.td`
  padding: 10px 12px;
  border-bottom: 1px solid ${color.borderLightest};
  color: ${color.textDark};
  ${font.size(13.5)}
  ${mixin.truncateText}
`;

export const WorkCell = styled(Cell)`
  vertical-align: middle;
`;

export const WorkCellContent = styled.div`
  display: flex;
  align-items: center;
`;

export const IssueKey = styled(Link)`
  margin-left: 8px;
  margin-right: 8px;
  color: ${color.textLink};
  ${font.medium}
  ${font.size(13)}
  &:hover {
    text-decoration: underline;
  }
`;

export const IssueTitle = styled.div`
  min-width: 0;
  ${mixin.truncateText}
`;

export const UserCell = styled(Cell)`
  vertical-align: middle;
`;

export const UserCellContent = styled.div`
  display: flex;
  align-items: center;
`;

export const UserName = styled.span`
  margin-left: 8px;
  ${mixin.truncateText}
`;

export const PriorityCell = styled(Cell)`
  vertical-align: middle;
`;

export const PriorityCellContent = styled.div`
  display: flex;
  align-items: center;

  & > span {
    margin-left: 6px;
  }
`;

export const StatusCell = styled(Cell)`
  padding-top: 6px;
  padding-bottom: 6px;
`;

export const StatusSelect = styled(Select)`
  width: 200px;
`;

export const StatusTag = styled.div`
  text-transform: uppercase;
  transition: all 0.1s;
  ${props => mixin.tag(issueStatusBackgroundColors[props.color], issueStatusColors[props.color])}
  ${props =>
    props.isValue &&
    css`
      height: 28px;
      padding: 0 8px;
      ${font.size(11.5)}
      & > div {
        margin-right: 3px;
      }
    `}
`;

export const MutedCell = styled(Cell)`
  color: ${color.textMedium};
`;

export const Checkbox = styled.input`
  position: relative;
  top: 1px;
`;

export const RowActions = styled(Cell)`
  color: ${color.textLight};
  text-align: center;
  ${mixin.clickable}
`;

export const EmptyState = styled.div`
  padding: 20px;
  color: ${color.textMedium};
  text-align: center;
  ${font.size(14)}
`;
