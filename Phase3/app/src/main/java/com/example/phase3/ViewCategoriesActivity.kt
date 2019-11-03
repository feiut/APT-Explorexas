package com.example.phase3

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.ListView
import android.widget.SimpleAdapter
import android.R.drawable.presence_online
import android.R.drawable.presence_offline
import android.util.Log
import android.view.View
import android.widget.ImageView
import com.android.volley.Request
import com.android.volley.Response
import com.android.volley.toolbox.Volley
import com.android.volley.toolbox.StringRequest
import kotlinx.android.synthetic.main.activity_view_categories.*
import com.google.gson.*

class ViewCategoriesActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_view_categories)

        val queue = Volley.newRequestQueue(this)
        // 2. Create the request with the callback
        val url = getString(R.string.website_url)
        val stringRequest = StringRequest(Request.Method.GET, url,
            Response.Listener {
                    response -> Log.d("soap_request", response)
            },
            Response.ErrorListener {
                error -> run {
                    txtHeader.text = "Failed to retrieve data"
                    lstCategories.visibility = View.GONE
                    Log.d("error", error.toString())
                }
            })
        queue.add(stringRequest)




class ViewCategoriesActivity : AppCompatActivity() {
    fun bind(categories:JsonArray) {
        Log.d("debug", categories.toString())

        val aList = ArrayList<HashMap<String, String>>()

        for (i in 0 until categories.size()) {
            val hm = HashMap<String, String>()
            val item = categories.get(i).getAsJsonObject()
            hm["listview_title"] = item.get("catName").toString()
            hm["listview_discription"] = item.get("catDescription").toString()
            hm["listview_image"] = Integer.toString(presence_online)
            hm["listview_imageid"] = item.get("imageId").toString()
            aList.add(hm)
        }

        val from = arrayOf("listview_image", "listview_title", "listview_discription")
        val to = intArrayOf(
            R.id.listview_image,
            R.id.listview_item_title,
            R.id.listview_item_short_description
        )

        val simpleAdapter = SimpleAdapter(baseContext, aList, R.layout.listview_activity, from, to)
        val androidListView = findViewById(R.id.lstCategories) as ListView
        androidListView.setAdapter(simpleAdapter)

        val firstPosition = androidListView.getFirstVisiblePosition() - androidListView.getHeaderViewsCount()
        for (rowid in 0 until categories.size()) {
            val wantedChild = rowid - firstPosition
            if (wantedChild < 0 || wantedChild >= androidListView.getChildCount()) {
                continue
            }
            Log.d("wantedChild", wantedChild.toString())
            val item = androidListView.getChildAt(wantedChild)
            Log.d("item", item.toString())
            val image = item.findViewById<ImageView>(R.id.listview_image)
            val imageUrl = aList[rowid]["listview_imageid"]
            Log.d("image", imageUrl)

        }
    }
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_view_categories)

        val queue = Volley.newRequestQueue(this)
        // 2. Create the request with the callback
        val url = "http://apt-team7.appspot.com"
        val stringRequest = StringRequest(Request.Method.GET, url,
            Response.Listener {
                response -> run {
                val parser = JsonParser()
                val jsonTree = parser.parse(response)
                val categories = jsonTree.asJsonArray
                bind(categories)
                }
            },
            Response.ErrorListener {
                error -> run {
                    txtHeader.text = "Failed to retrieve data"
                    lstCategories.visibility = View.GONE
                    Log.d("error", error.toString())
                }
            })
        queue.add(stringRequest)
    }
}
