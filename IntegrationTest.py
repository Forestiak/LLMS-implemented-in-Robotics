import unittest
from unittest.mock import patch, MagicMock
import logging
from RobotService import RobotService  # Replace with the actual path to your RobotService class

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TestRobotServiceIntegration(unittest.TestCase):

    @patch('RobotService.SimulationService')  # Mock SimulationService
    @patch('RobotService.YOLOService')  # Mock YOLOService
    @patch('RobotService.OpenAIVoiceToTextService')  # Mock VoiceToTextService
    @patch('RobotService.LLMManager')  # Mock LLMManager
    def test_perform_task(self, MockLLMManager, MockVoiceToTextService, MockYOLOService, MockSimulationService):
        logger.info("Starting test_perform_task")

        # Setup the mock objects and their return values
        mock_simulation_service = MockSimulationService.return_value
        mock_simulation_service.GetImage.return_value = (MagicMock(), MagicMock())
        logger.debug("Mock SimulationService configured")

        mock_yolo_service = MockYOLOService.return_value
        mock_yolo_service.RecognizeObjects.return_value = (['object1', 'object2'], ['box1', 'box2'])
        logger.debug("Mock YOLOService configured")

        mock_voice_to_text_service = MockVoiceToTextService.return_value
        mock_voice_to_text_service.GetText.return_value = "User speech text"
        logger.debug("Mock VoiceToTextService configured")

        mock_llm_manager = MockLLMManager.return_value
        mock_llm_manager.process_input.return_value = {
            "commands": [
                {"command": "LOCATE_OBJECT", "parameters": []},
                {"command": "GRASP_OBJECT", "parameters": ["item_object"]}
            ],
            "text": "Here is what you need to do..."
        }
        logger.debug("Mock LLMManager configured")

        # Initialize RobotService
        robot_service = RobotService()
        robot_service.stt = mock_voice_to_text_service

        # Call PerformTask
        detected_objects = ['object1', 'object2']
        robot_service.PerformTask(detected_objects)
        logger.debug("PerformTask method called")

        # Verify interactions and responses
        mock_voice_to_text_service.GetText.assert_called_once()
        mock_llm_manager.process_input.assert_called_once_with("User speech text", detected_objects)

        # Logging the results
        logger.info("VoiceToTextService GetText called once - Ensure data flow between components verified")
        logger.info("LLMManager process_input called with user speech text and detected objects - Verify component interactions verified")

        logger.debug(f"User input: {mock_voice_to_text_service.GetText.return_value}")
        logger.debug(f"Processed response: {mock_llm_manager.process_input.return_value}")

    @patch('RobotService.SimulationService')  # Mock SimulationService
    @patch('RobotService.YOLOService')  # Mock YOLOService
    def test_grasp(self, MockYOLOService, MockSimulationService):
        logger.info("Starting test_grasp")

        # Setup the mock objects and their return values
        mock_simulation_service = MockSimulationService.return_value
        mock_simulation_service.GetImage.return_value = (MagicMock(), MagicMock())
        logger.debug("Mock SimulationService configured")

        mock_yolo_service = MockYOLOService.return_value
        mock_yolo_service.RecognizeObjects.return_value = (['object1', 'object2'], ['box1', 'box2'])
        logger.debug("Mock YOLOService configured")

        # Initialize RobotService
        robot_service = RobotService()
        robot_service.simulationService = mock_simulation_service
        robot_service.yoloService = mock_yolo_service

        # Call grasp
        robot_service.grasp()
        logger.debug("Grasp method called")

        # Verify interactions and responses
        mock_simulation_service.GetImage.assert_called_once()
        mock_yolo_service.RecognizeObjects.assert_called_once()

        logger.info("SimulationService GetImage called once - Ensure data flow between components verified")
        logger.info("YOLOService RecognizeObjects called once - Verify component interactions verified")

        # Logging the results
        logger.debug(f"Detected objects: {mock_yolo_service.RecognizeObjects.return_value[0]}")
        logger.debug(f"Bounding boxes: {mock_yolo_service.RecognizeObjects.return_value[1]}")

if __name__ == '__main__':
    unittest.main()
