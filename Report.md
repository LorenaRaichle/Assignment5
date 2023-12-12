Assignment 5 
---------------------

# Team Members

- Joey & Lorena

# GitHub link to your (forked) repository

https://github.com/LorenaRaichle/Assignment5

# Task 1

Note: Some questions require you to take screenshots. In that case, please join the screenshots and indicate in your answer which image refer to which screenshot.

1. What happens when Raft starts? Why?

Ans: Raft divides the consensus problem into 3 sub-problems. The first step is the leader election among all nodes (starting as followers) since every action (client request)/delivering of messages (log replications) will be performed through the leader.
Every node/ state machine has its own logical clock. When starting in the first term, each follower node starts a randomized election timeout (The timeout is randomized to avoid several elections at the same time) which is the time waiting until it becomes a candidate.
We are suspecting no leader after the randomized timeout passed without any communication from the leader.
Then the node passes from the follower state to the candidate state and sends vote requests to all the other remaining follower nodes within the cluster.
The candidate node votes for itself and waits for the response messages of the other nodes. If a majority of nodes replied, the candidate becomes leader of the term.
The leader then sends heartbeats to the followers for a permanent communication. If the leader is down and does not send any heartbeats, one of the randomized timeouts of the followers expires and a new leader is elected. 



2. Perform one request on the leader, wait until the leader is committed by all servers. Pause the simulation.
Then perform a new request on the leader. Take a screenshot, stop the leader and then resume the simulation.
Once, there is a new leader, perform a new request and then resume the previous leader. Once, this new request is committed by all servers, pause the simulation and take a screenshot. Explain what happened?

Ans: In Screenshot "task1 q2 1.png" all nodes are in term 2, S2 was elected the leader node in this term and the replication of log entries after sending a request was successful.
The leader committed the operation successfully which is indicated by the solid line and the logs in all nodes are up-to-date and consistent.
The second operation was initiated but not committed before the leader has been stopped (it was not replicated to a majority of nodes and therefore not committed), indicated with the non-solid line around the log of the leader S2. 
Since leader node S2 has been stopped, there are no heartbeats anymore and there is a timeout with a new leader election.
S5 becomes the new leader of term3, while node 2 is still paused. 
After initiating a new client request, a log entry for term 3 is created and replicated to all nodes in the cluster. Since a majority of nodes have written the entry to their logs, it's committed successfully (solid), the uncommitted log entry from the previous leader S2 has been overwritten (see "task1 q2 2.png").
In this way, uncommitted entries from past terms do not cause any conflicts and consistency is ensured.
The "Log Marching Property" (slides "08-DS-Fault-tolerance-consensus", p. 37) is respected as any conflicts (such as the uncommitted entry from the old leader S2), will be deleted or overwritten to ensure all nodes have identical logs up to the index of the last committed entry.
Hence, the leader always has the most up-to-date log and the majority of nodes maintain consistent replicated logs across the cluster, even in case of the failure of a leader, as shown in the example.


3. Stop the current leader and two other servers. After a few increase in the Raft term, pause the simulation and take a screenshot. Then resume all servers and restart the simulation. After the leader election, pause the simulation and take a screenshot. Explain what happened.

Ans: The Screenshot "task1 q3 1.png" shows the term increment to 6 with only S4 and S3 running. The term increment indicates that there were multiple rounds of a leader election between node S4 and S3 that were not successful since there was no consensus possible, leading to a new leader election.
Since Raft needs the majority of the nodes for a consensus and in this case only 2 out of the 5 nodes in the cluster were active, there was no consensus and no leader election possible.
For this reason, no new committed operations have been registered in the log entries. 
Screenshot "task1 q3 2.png" shows that after resuming the nodes, a majority of nodes was active again, a consensus could be reached and S3 was elected as the new leader of term 6. 
In conclusion, the Raft algorithm ensures that despite failures and the unavailability of a majority, the system can recover and continue processing new operations once the majority of nodes are back. 


# Task 2

1. Indicate the replies that you get from the "/admin/status" endpoint of the HTTP service for each servers. Which server is the leader? Can there be multiple leaders?

Ans: We can inspect the status information of the "/admin/status" endpoint for each server to determine the leader. After inspection, the leader (IP: 127.0.0.1 and Port 6000) appears in all the output, indicating that it is the leader. There can only be one leader at a time / in a term in a consensus-based distributed system. If there are multiple leaders, it will likely result in an inconsistency in the distributed state. 

2. Perform a Put request for the key ``a" on the leader. What is the new status? What changes occurred and why (if any)?

Ans: When a PUT request is performed, it will trigger a write operation. Hence, the key-value store's log will have a new entry and others nodes in the system will be replicated the same operation to maintain consistency. The status will show the updated values (apple, banana) associated with the key "a". 
In the provided screenshots task2_2PUTon0_GETon1.png for example, a put operation (apple, banana) is performed on server 0. 
With a GET operation with the same key on server 1, we can see that the PUT operation was replicated.

3. Perform an Append request for the key ``a" on the leader. What is the new status? What changes occurred and why (if any)?

Ans: When an APPEND request is performed, it will append data to the existing value associated with the key "a" from the leader. The key-value store's log will be appended with a new entry and this change will be replicated to other nodes in the system. The status will show the updated values (cat, dog, mouse) associated with the key "a".

4. Perform a Get request for the key ``a" on the leader. What is the new status? What change (if any) happened and why?

Ans: When a GET request is performed, it will retrieve the last values (cat, dog, mouse) associated with the key "a" from the leader. As this is a read-only operation, the status will not change. 



# Task 3

1. Shut down the server that acts as a leader. Report the status that you get from the servers that remain active after shutting down the leader.

Ans: The status shows that the leader is down and a new leader has already been elected. After the shutdown a the random timeout of one of the other servers, there is a new leader election.
As visible in the screenshot task3.1LeaderShutDown.png, the leader was node "127.0.0.1:6000". 
After the shutdown, both still available servers (6001 & 6002) indicate "127.0.0.1:6001" as the leader (one of the node indicates itself as the leader). The election already happened and the new leader is already reported. 

 2. Perform a Put request for the key "a". Then, restart the server from the previous point, and indicate the new status for the three servers. Indicate the result of a Get request for the key ``a" to the previous leader.

Ans: When the PUT request is performed, the status should show an updated value, and the log will have a new entry. Server 8080 has been shut down in task 3.1, a PUT request has been performed during shutdown, now the node is up again and indicates the same new leader as well as the other 2 servers that were still available (see screenshot task3.2_restart.png). 
When rejoining the cluster again, the shutdown server receives the updates about the new leader and the new logs. For this reason, the new key is also included and the cluster is consistent again. 
After the GET request, the previous shutdown server returns the new value as well indicating that the data replication took place and was successful. 


3. Has the Put request been replicated? Indicate which steps lead to a new election and which ones do not. Justify your answer using the statuses returned by the servers.

Ans: The PUT request has been replicated to all nodes including the node that is rejoining the cluster after the shutdown. 
When a leader is down and there are no more heartbeat messages sent from the leader, the leader election happens immediately after the randomized timeout (to avoid split votes) of a node since all transactions are replicated by the leader. Without a leader, no further progress is possible in the cluster. 
Only servers are involved in the election process and all request types from the client do not affect or lead to a leader election.

4. Shut down two servers, including the leader --- starting with the server that is not the leader. Report the status of the remaining servers and explain what happened.

Ans: If 2 out of 3 total servers are down, including the leader, there is no majority of nodes available in the cluster and there cannot be a new leader election. 
The remaining available server can never leave the follower or candidate state as long as the majority of the nodes are not available in the system.

5. Can you perform Get, Put, or Append requests in this system state? Justify your answer.

Ans: After shutting down the majority of servers, the system is not able to handle the Get, Put, or Append requests properly.
This is due to the fact that the system requires a leader to further process these requests and replicate the logs across the cluster. 


6. Restart the servers and note down the new status. Describe what happened.

Ans: Once the servers are shut down including the leader and they rejoin the cluster, this will trigger a new leader election.
As soon as there is a new leader, the cluster operates as expected and is able to process requests from the client and replicate them across the cluster.
The status indicates that the election was successful and that the cluster has come to a consensus in terms of the new leader election.



# Task 4

1. What is a consensus algorithm? What are they used for in the context of replicated state machines? 

Ans: The replication of state machines is a general approach to build fault-tolerant systems with consensus algorithms like Paxos or Raft.
A consensus algorithm is a deterministic algorithm, where every server is in a specific state at any point in time and holds a state machine and a log.
The consensus algorithm only makes progress, if the majority of the state machines are available. If the majority of servers is down, there would be no progress but the algorithm would never return an incorrect and inconsistent result.
For the clients it appears as if the interaction was only with one state machine, not with a distributed system. 
The general idea is to maintain a consistent state across multiple replicas that can serve as backups in the case of system failures. In this way, consistency and fault-tolerance is ensured with Raft and Paxos as partially synchronous crash recovery models.


2. (0.5pt) What are the main features of the Raft algorithm? How does Raft enable fault tolerance?

Ans: The Raft algorithm divides the consensus problem into 3 sub-problems: Leader election, log replication and ensuring safety (slides "08-DS-Fault-tolerance-consensus", p. 39).
For the leader election, Raft uses a randomized time out. If for a certain time there was no heartbeat / communication with the leader, followers can become a candidate themselves and request votes from the others to become the leader.
The leader then handles log replications, meaning that if there was a request from a client, the leader appends that to its log and replicates its own log to other followers. In this way, Raft maintains a consistent replicated log across all nodes. Additionally, a entry is only committed if it is present on a majority of nodes.
For safety reasons, a node can only become the leader, if its logs are up-to-date and contain all previous committed operations. 

3. What are Byzantine failures? Can Raft handle them?

Ans: Byzantine failures are connected to the "Byzantine generals problem" which is, as well as the "two generals problem", a fault experiment. 
While the "two generals problem" states that there is no certainty in a distributed system that a message has been received, the "byzantine problem" states that there is a reliable communication. 
However, some generals / nodes might be malicious and behave in an unexpected manner.
Raft is not designed to handle Byzantine failures since nodes will stop and not proceed instead of returning an incorrect and inconsistent result. Raft is not able to deal with sending false messages and other byzantine problems. 