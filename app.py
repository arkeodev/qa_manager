"""Streamlit UI for the MAS simulation using Microsoft Autogen."""

import logging

import streamlit as st

from autogen import GroupChat, GroupChatManager
from agents.agent_factory import create_agents
from utils.logging_utils import setup_logging
from utils.helper_functions import is_termination_msg


def main():
    """Streamlit app main function for the MAS simulation."""
    setup_logging()
    logger = logging.getLogger('StreamlitApp')

    st.title("Multi-Agent System Simulation for QA and Testing")

    # Define LLM configuration
    llm_config = {
        "config_list": [{"model": "gpt-4o-mini"}],
        "temperature": st.slider("Select Temperature", 0.0, 1.0, 0.7, 0.1),
    }

    # Initialize session state
    if 'agents' not in st.session_state:
        st.session_state.agents = create_agents(llm_config)

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    if st.button("Run Simulation"):
        logger.info("Running MAS simulation.")

        # Create a group chat
        group_chat = GroupChat(
            agents=list(st.session_state.agents.values()),
            messages=st.session_state.chat_history,
            max_round=50,
        )

        # Create a group chat manager
        manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)

        # Start the conversation
        qa_manager_agent = st.session_state.agents["qa_manager_agent"]
        task_message = (
            "Initiate the QA process for the new web application release. "
            "Please develop test plans and strategies based on the project requirements. "
            "Allocate resources and assign tasks to Tester Agents."
        )

        chat_result = qa_manager_agent.initiate_chat(
            manager,
            message=task_message,
            is_termination_msg=is_termination_msg,
        )

        # Update chat history
        st.session_state.chat_history = chat_result.chat_history

        st.success("Simulation completed.")

    # Display chat history
    st.header("Chat History")
    for message in st.session_state.get('chat_history', []):
        if 'name' in message:
            st.write(f"**{message['name']}**: {message['content']}")
        else:
            st.write(f"{message['content']}")


if __name__ == "__main__":
    main()
