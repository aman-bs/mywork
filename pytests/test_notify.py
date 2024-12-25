from augmet_cli.fil2   

with patch("augmet.jobs.interface.push_to_db") as mock_push_to_db:
        mock_db_response = MagicMock()
        mock_db_response.status_code = 200
        mock_db_response.message = "DB call successful!!"
        mock_push_to_db.return_value = mock_db_response

        assert mock_push_to_db is not None
        response = augmet_sample_run_obj.notify(dummy_job, "Test Notification")

        assert response == mock_db_response
        print(mock_push_to_db.call_args)
        mock_push_to_db.assert_called_once()
