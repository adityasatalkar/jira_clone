import React, { Fragment } from 'react';
import PropTypes from 'prop-types';
import { Link, useRouteMatch } from 'react-router-dom';
import { xor } from 'lodash';

import useApi from 'shared/hooks/api';
import useCurrentUser from 'shared/hooks/currentUser';
import useMergeState from 'shared/hooks/mergeState';
import api from 'shared/utils/api';
import { formatDateTime } from 'shared/utils/dateTime';
import { updateArrayItemById } from 'shared/utils/javascript';
import { IssuePriorityCopy, IssueStatus, IssueStatusCopy } from 'shared/constants/issues';
import {
  Breadcrumbs,
  PageError,
  PageLoader,
  InputDebounced,
  Avatar,
  Button,
  IssueTypeIcon,
  IssuePriorityIcon,
  Icon,
} from 'shared/components';

import IssueDetailsPage from './IssueDetailsPage';
import {
  ViewHeader,
  HeaderTitles,
  Heading,
  Subheading,
  Toolbar,
  SearchInput,
  AvatarFilters,
  AvatarIsActiveBorder,
  ToolbarAvatar,
  ToolbarActions,
  FilterButton,
  ClearAll,
  TableContainer,
  Table,
  ColumnHeader,
  Cell,
  WorkCell,
  WorkCellContent,
  IssueKey,
  IssueTitle,
  UserCell,
  UserCellContent,
  UserName,
  PriorityCell,
  PriorityCellContent,
  StatusCell,
  StatusSelect,
  StatusTag,
  EmptyState,
  MutedCell,
  Checkbox,
  RowActions,
} from './Styles';

const propTypes = {
  project: PropTypes.object.isRequired,
  fetchProject: PropTypes.func.isRequired,
  updateLocalProjectIssues: PropTypes.func.isRequired,
};

const defaultFilters = {
  searchTerm: '',
  userIds: [],
  myOnly: false,
  status: 'all',
};

const ProjectListView = ({ project, fetchProject, updateLocalProjectIssues }) => {
  const match = useRouteMatch();
  const issueDetailsMatch = useRouteMatch(`${match.path}/issues/:issueId`);

  const [{ data, error, setLocalData }] = useApi.get('/issues');
  const { currentUserId } = useCurrentUser();

  const [filters, mergeFilters] = useMergeState(defaultFilters);

  const projectUsers = Array.isArray(project.users) ? project.users : [];

  const updateIssueLocally = (issueId, updatedFields) => {
    setLocalData(currentData => {
      if (!currentData || !Array.isArray(currentData.issues)) {
        return currentData;
      }
      return {
        issues: updateArrayItemById(currentData.issues, issueId, updatedFields),
      };
    });
    updateLocalProjectIssues(issueId, updatedFields);
  };

  if (issueDetailsMatch) {
    return (
      <IssueDetailsPage
        issueId={issueDetailsMatch.params.issueId}
        listPath={match.url}
        project={project}
        projectUsers={projectUsers}
        fetchProject={fetchProject}
        updateIssueLocally={updateIssueLocally}
      />
    );
  }

  if (!data) return <PageLoader />;
  if (error) return <PageError />;

  const allIssues = Array.isArray(data.issues) ? data.issues : [];
  const usersById = projectUsers.reduce((result, user) => {
    result[user.id] = user;
    return result;
  }, {});

  const issues = getFilteredIssues(allIssues, filters, currentUserId);

  const updateIssueStatus = (issue, status) => {
    if (issue.status === status) return;

    api.optimisticUpdate(`/issues/${issue.id}`, {
      updatedFields: {
        status,
        listPosition: calculateNextListPosition(allIssues, status),
      },
      currentFields: issue,
      setLocalData: fields => updateIssueLocally(issue.id, fields),
    });
  };

  const boardPath = match.url.replace('/list', '/board');

  return (
    <Fragment>
      <Breadcrumbs items={['Projects', project.name, 'List view']} />

      <ViewHeader>
        <HeaderTitles>
          <Heading>Task list view</Heading>
          <Subheading>{`${issues.length} issues`}</Subheading>
        </HeaderTitles>
        <Link to={boardPath}>
          <Button icon="board">Switch to board</Button>
        </Link>
      </ViewHeader>

      <Toolbar>
        <SearchInput>
          <InputDebounced
            icon="search"
            value={filters.searchTerm}
            onChange={searchTerm => mergeFilters({ searchTerm })}
            placeholder="Search work"
          />
        </SearchInput>

        <AvatarFilters>
          {projectUsers.map(user => (
            <AvatarIsActiveBorder key={user.id} isActive={filters.userIds.includes(user.id)}>
              <ToolbarAvatar
                avatarUrl={user.avatarUrl}
                name={user.name}
                onClick={() => mergeFilters({ userIds: xor(filters.userIds, [user.id]) })}
              />
            </AvatarIsActiveBorder>
          ))}
        </AvatarFilters>

        <ToolbarActions>
          <FilterButton
            variant="secondary"
            isActive={filters.myOnly}
            onClick={() => mergeFilters({ myOnly: !filters.myOnly })}
          >
            Only my tasks
          </FilterButton>

          <FilterButton
            variant="secondary"
            isActive={filters.status === 'all'}
            onClick={() => mergeFilters({ status: 'all' })}
          >
            All
          </FilterButton>
          {Object.values(IssueStatus).map(status => (
            <FilterButton
              key={status}
              variant="secondary"
              isActive={filters.status === status}
              onClick={() => mergeFilters({ status })}
            >
              {IssueStatusCopy[status]}
            </FilterButton>
          ))}

          {(filters.searchTerm ||
            filters.userIds.length > 0 ||
            filters.myOnly ||
            filters.status !== 'all') && (
            <ClearAll onClick={() => mergeFilters(defaultFilters)}>Clear all</ClearAll>
          )}
        </ToolbarActions>
      </Toolbar>

      <TableContainer>
        <Table>
          <thead>
            <tr>
              <ColumnHeader width={34}>
                <Checkbox type="checkbox" readOnly />
              </ColumnHeader>
              <ColumnHeader>Work</ColumnHeader>
              <ColumnHeader>Assignee</ColumnHeader>
              <ColumnHeader>Reporter</ColumnHeader>
              <ColumnHeader>Priority</ColumnHeader>
              <ColumnHeader>Status</ColumnHeader>
              <ColumnHeader>Created</ColumnHeader>
              <ColumnHeader>Updated</ColumnHeader>
              <ColumnHeader>Resolution</ColumnHeader>
              <ColumnHeader width={45}> </ColumnHeader>
            </tr>
          </thead>

          <tbody>
            {issues.map(issue => {
              const issueUserIds = getIssueUserIds(issue);
              const assignee = usersById[issueUserIds[0]];
              const reporter = usersById[issue.reporterId];

              return (
                <tr key={issue.id}>
                  <Cell>
                    <Checkbox type="checkbox" readOnly />
                  </Cell>

                  <WorkCell>
                    <WorkCellContent>
                      <IssueTypeIcon type={issue.type} size={16} top={1} />
                      <IssueKey
                        to={`${match.url}/issues/${issue.id}`}
                      >{`MFD-${issue.id}`}</IssueKey>
                      <IssueTitle>{issue.title}</IssueTitle>
                    </WorkCellContent>
                  </WorkCell>

                  <UserCell>
                    <UserCellContent>{renderUser(assignee)}</UserCellContent>
                  </UserCell>
                  <UserCell>
                    <UserCellContent>{renderUser(reporter)}</UserCellContent>
                  </UserCell>

                  <PriorityCell>
                    <PriorityCellContent>
                      <IssuePriorityIcon priority={issue.priority} top={-1} />
                      <span>{IssuePriorityCopy[issue.priority]}</span>
                    </PriorityCellContent>
                  </PriorityCell>

                  <StatusCell>
                    <StatusSelect
                      variant="empty"
                      dropdownWidth={210}
                      withClearValue={false}
                      name={`issue-status-${issue.id}`}
                      value={issue.status}
                      options={Object.values(IssueStatus).map(status => ({
                        value: status,
                        label: IssueStatusCopy[status],
                      }))}
                      onChange={status => updateIssueStatus(issue, status)}
                      renderValue={({ value: status }) => (
                        <StatusTag isValue color={status}>
                          <div>{IssueStatusCopy[status]}</div>
                          <Icon type="chevron-down" size={18} />
                        </StatusTag>
                      )}
                      renderOption={({ value: status }) => (
                        <StatusTag color={status}>{IssueStatusCopy[status]}</StatusTag>
                      )}
                    />
                  </StatusCell>

                  <Cell>{formatDateOrFallback(issue.createdAt)}</Cell>
                  <Cell>{formatDateOrFallback(issue.updatedAt)}</Cell>
                  <MutedCell>Unresolved</MutedCell>

                  <RowActions>
                    <Icon type="more" size={18} />
                  </RowActions>
                </tr>
              );
            })}
          </tbody>
        </Table>

        {issues.length === 0 && <EmptyState>No issues match your current filters.</EmptyState>}
      </TableContainer>
    </Fragment>
  );
};

const renderUser = user =>
  user ? (
    <Fragment>
      <Avatar size={22} avatarUrl={user.avatarUrl} name={user.name} />
      <UserName>{user.name}</UserName>
    </Fragment>
  ) : (
    <Fragment>
      <Avatar size={22} name="U" />
      <UserName>Unassigned</UserName>
    </Fragment>
  );

const getFilteredIssues = (issues, filters, currentUserId) => {
  const { searchTerm, userIds, myOnly, status } = filters;

  let filteredIssues = [...issues].sort((a, b) =>
    getDateSortValue(b.updatedAt).localeCompare(getDateSortValue(a.updatedAt)),
  );

  if (searchTerm) {
    const loweredSearchTerm = searchTerm.toLowerCase();
    filteredIssues = filteredIssues.filter(issue => {
      const searchableValues = [
        issue.title,
        issue.descriptionText,
        issue.description,
        `mfd-${issue.id}`,
      ]
        .filter(Boolean)
        .join(' ')
        .toLowerCase();

      return searchableValues.includes(loweredSearchTerm);
    });
  }

  if (status !== 'all') {
    filteredIssues = filteredIssues.filter(issue => issue.status === status);
  }

  if (userIds.length > 0) {
    filteredIssues = filteredIssues.filter(issue =>
      getIssueUserIds(issue).some(userId => userIds.includes(userId)),
    );
  }

  if (myOnly && currentUserId) {
    filteredIssues = filteredIssues.filter(issue => getIssueUserIds(issue).includes(currentUserId));
  }

  return filteredIssues;
};

const calculateNextListPosition = (issues, status) => {
  const listPositions = issues
    .filter(issue => issue.status === status)
    .map(issue => issue.listPosition);

  if (listPositions.length === 0) {
    return 1;
  }

  return Math.min(...listPositions) - 1;
};

const getIssueUserIds = issue => (Array.isArray(issue.userIds) ? issue.userIds : []);

const getDateSortValue = value => (typeof value === 'string' ? value : '');

const formatDateOrFallback = value => (value ? formatDateTime(value, 'MMM D, YYYY h:mm A') : 'N/A');

ProjectListView.propTypes = propTypes;

export default ProjectListView;
