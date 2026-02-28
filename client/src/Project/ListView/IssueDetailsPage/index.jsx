import React, { Fragment } from 'react';
import PropTypes from 'prop-types';
import { useHistory } from 'react-router-dom';

import api from 'shared/utils/api';
import useApi from 'shared/hooks/api';
import { Breadcrumbs, CopyLinkButton, PageError, PageLoader } from 'shared/components';

import Type from '../../Board/IssueDetails/Type';
import Delete from '../../Board/IssueDetails/Delete';
import Title from '../../Board/IssueDetails/Title';
import Description from '../../Board/IssueDetails/Description';
import Comments from '../../Board/IssueDetails/Comments';
import Status from '../../Board/IssueDetails/Status';
import AssigneesReporter from '../../Board/IssueDetails/AssigneesReporter';
import Priority from '../../Board/IssueDetails/Priority';
import EstimateTracking from '../../Board/IssueDetails/EstimateTracking';
import Dates from '../../Board/IssueDetails/Dates';
import {
  DetailsSurface,
  DetailsTop,
  DetailsTopLeft,
  DetailsTopRight,
  BackButton,
  IssueKey,
  DetailsContent,
  DetailsMain,
  CommentsBlock,
  DetailsSidebar,
  SidebarCard,
} from './Styles';

const propTypes = {
  issueId: PropTypes.string.isRequired,
  listPath: PropTypes.string.isRequired,
  project: PropTypes.object.isRequired,
  projectUsers: PropTypes.array.isRequired,
  fetchProject: PropTypes.func.isRequired,
  updateIssueLocally: PropTypes.func.isRequired,
};

const ProjectListIssueDetailsPage = ({
  issueId,
  listPath,
  project,
  projectUsers,
  fetchProject,
  updateIssueLocally,
}) => {
  const history = useHistory();
  const [{ data, error, setLocalData }, fetchIssue] = useApi.get(`/issues/${issueId}`);

  const issueKey = `MFD-${issueId}`;
  const handleBack = () => history.push(listPath);

  if (!data) {
    return (
      <Fragment>
        <Breadcrumbs items={['Projects', project.name, 'List view', issueKey]} />
        <PageLoader />
      </Fragment>
    );
  }

  if (error) {
    return (
      <Fragment>
        <Breadcrumbs items={['Projects', project.name, 'List view', issueKey]} />
        <PageError />
      </Fragment>
    );
  }

  const { issue } = data;

  const updateLocalIssueDetails = fields =>
    setLocalData(currentData => ({ issue: { ...currentData.issue, ...fields } }));

  const updateIssue = updatedFields => {
    api.optimisticUpdate(`/issues/${issueId}`, {
      updatedFields,
      currentFields: issue,
      setLocalData: fields => {
        updateLocalIssueDetails(fields);
        updateIssueLocally(issue.id, fields);
      },
    });
  };

  return (
    <Fragment>
      <Breadcrumbs items={['Projects', project.name, 'List view', `MFD-${issue.id}`]} />

      <DetailsSurface>
        <DetailsTop>
          <DetailsTopLeft>
            <BackButton icon="arrow-left" variant="empty" onClick={handleBack}>
              Back to list
            </BackButton>
            <IssueKey>{`MFD-${issue.id}`}</IssueKey>
          </DetailsTopLeft>

          <DetailsTopRight>
            <Type issue={issue} updateIssue={updateIssue} />
            <CopyLinkButton variant="secondary" />
            <Delete issue={issue} fetchProject={fetchProject} modalClose={handleBack} />
          </DetailsTopRight>
        </DetailsTop>

        <DetailsContent>
          <DetailsMain>
            <Title issue={issue} updateIssue={updateIssue} />
            <Description issue={issue} updateIssue={updateIssue} />
            <CommentsBlock>
              <Comments issue={issue} fetchIssue={fetchIssue} />
            </CommentsBlock>
          </DetailsMain>

          <DetailsSidebar>
            <SidebarCard>
              <Status issue={issue} updateIssue={updateIssue} />
              <AssigneesReporter
                issue={issue}
                updateIssue={updateIssue}
                projectUsers={projectUsers}
              />
              <Priority issue={issue} updateIssue={updateIssue} />
              <EstimateTracking issue={issue} updateIssue={updateIssue} />
              <Dates issue={issue} />
            </SidebarCard>
          </DetailsSidebar>
        </DetailsContent>
      </DetailsSurface>
    </Fragment>
  );
};

ProjectListIssueDetailsPage.propTypes = propTypes;

export default ProjectListIssueDetailsPage;
