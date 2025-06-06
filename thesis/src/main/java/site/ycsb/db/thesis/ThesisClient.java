package site.ycsb.db.thesis;

import site.ycsb.*;

import java.util.*;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;


/**
 * Binding for the Thesis database.
 *
 */
public class ThesisClient extends DB {

    //final static 

    @Override
    public void init() throws DBException {
        System.out.println("Initializing ThesisClient...");
    }

    @Override
    public void cleanup() throws DBException {
        System.out.println("Cleaning up ThesisClient...");
    }

    private void request(String endpoint, String json){
        try {
            URL url = new URL(endpoint);

            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setDoOutput(true);
            conn.setRequestMethod("POST");
            conn.setReadTimeout(1000);
            
            // set headers
            conn.setRequestProperty("Content-Type", "application/json");
            conn.setRequestProperty("Accept", "application/json");

            // set body
            System.out.println("JSON Input String: " + json);
            try(OutputStream os = conn.getOutputStream()) {
                byte[] input = json.getBytes("utf-8");
                os.write(input, 0, input.length);			
            }

            //Getting the response code
            int responsecode = conn.getResponseCode();

            System.out.println("Response Code: " + responsecode);

            System.out.println("Response Message: " + conn.getResponseMessage());

            if(responsecode > 299) {
                System.out.println("Error: " + conn.getResponseMessage());
                return;
            }

            try(BufferedReader br = new BufferedReader(
            new InputStreamReader(conn.getInputStream(), "utf-8"))) {
                StringBuilder response = new StringBuilder();
                String responseLine = null;
                while ((responseLine = br.readLine()) != null) {
                    response.append(responseLine.trim());
                }
                System.out.println(response.toString());
            } catch(Exception e) {
                e.printStackTrace();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Override
    public Status read(String table, String key, Set<String> fields, Map<String, ByteIterator> result) {
        System.out.println("Reading from ThesisClient: " + table + ", " + key);
        // Simulate a read operation
        result.put("field1", new ByteArrayByteIterator("value1".getBytes()));


        try {

            URL url = new URL("http://192.168.0.161:8080/api/get");

            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setDoOutput(true);
            conn.setRequestMethod("POST");
            conn.setReadTimeout(1000);
            
            // set headers
            conn.setRequestProperty("Content-Type", "application/json");
            conn.setRequestProperty("Accept", "application/json");

            // set body
            String jsonInputString = "{\"key\":\"test\",\"value\":\"test\"}";
            System.out.println("JSON Input String: " + jsonInputString);
            try(OutputStream os = conn.getOutputStream()) {
                byte[] input = jsonInputString.getBytes("utf-8");
                os.write(input, 0, input.length);			
            }

            //Getting the response code
            int responsecode = conn.getResponseCode();

            System.out.println("Response Code: " + responsecode);

            System.out.println("Response Message: " + conn.getResponseMessage());

            if(responsecode > 299) {
                System.out.println("Error: " + conn.getResponseMessage());
                return Status.ERROR;
            }

            try(BufferedReader br = new BufferedReader(
            new InputStreamReader(conn.getInputStream(), "utf-8"))) {
                StringBuilder response = new StringBuilder();
                String responseLine = null;
                while ((responseLine = br.readLine()) != null) {
                    response.append(responseLine.trim());
                }
                System.out.println(response.toString());
            } catch(Exception e) {
                e.printStackTrace();
            }

        } catch (Exception e) {
            e.printStackTrace();
        }


        return Status.OK;
    }

    @Override
    public Status update(String table, String key, Map<String, ByteIterator> values) {
        System.out.println("Updating in ThesisClient: " + table + ", " + key);
        // Simulate an update operation
        return Status.OK;
    }

    @Override
    public Status insert(String table, String key, Map<String, ByteIterator> values) {
        System.out.println("Inserting into ThesisClient: " + table + ", " + key);
        // Simulate an insert operation
        String jsonInputString = "{\"key\":\"" + key + "\", \"value\":\"test\"}";
        request("http://192.168.0.161:8080/api/insert", jsonInputString);
        return Status.OK;
    }

    @Override
    public Status delete(String table, String key) {
        System.out.println("Deleting from ThesisClient: " + table + ", " + key);
        // Simulate a delete operation
        return Status.OK;
    }

    @Override
    public Status scan(String table, String startkey, int recordcount, Set<String> fields, Vector<HashMap<String, ByteIterator>> result) {
        System.out.println("Scanning in ThesisClient: " + table + ", starting from " + startkey + ", count: " + recordcount);
        // Simulate a scan operation
        return Status.OK;
    }
}