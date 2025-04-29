// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract DAOCouncil {

    enum Decision { Pending, Approved, Rejected }

    struct Proposal {
        uint id;
        string title;
        string description;
        uint votesApprove;
        uint votesReject;
        Decision finalDecision;
    }

    uint public nextProposalId = 1;
    mapping(uint => Proposal) public proposals;

    event ProposalSubmitted(uint proposalId, string title);
    event Voted(uint proposalId, string voter, bool approve);
    event Finalized(uint proposalId, Decision decision);

    function submitProposal(string memory _title, string memory _description) public returns (uint) {
        Proposal storage p = proposals[nextProposalId];
        p.id = nextProposalId;
        p.title = _title;
        p.description = _description;
        p.votesApprove = 0;
        p.votesReject = 0;
        p.finalDecision = Decision.Pending;
        emit ProposalSubmitted(nextProposalId, _title);
        nextProposalId++;
        return p.id;
    }

    function vote(uint _proposalId, string memory _voterName, bool _approve) public {
        Proposal storage p = proposals[_proposalId];
        require(p.id != 0, "Proposal not found");
        require(p.finalDecision == Decision.Pending, "Proposal already finalized");

        if (_approve) {
            p.votesApprove++;
        } else {
            p.votesReject++;
        }

        emit Voted(_proposalId, _voterName, _approve);
    }

    function finalizeProposal(uint _proposalId) public {
        Proposal storage p = proposals[_proposalId];
        require(p.id != 0, "Proposal not found");
        require(p.finalDecision == Decision.Pending, "Already finalized");

        if (p.votesApprove > p.votesReject) {
            p.finalDecision = Decision.Approved;
        } else {
            p.finalDecision = Decision.Rejected;
        }

        emit Finalized(_proposalId, p.finalDecision);
    }

    function getProposal(uint _proposalId) public view returns (Proposal memory) {
        return proposals[_proposalId];
    }
}
