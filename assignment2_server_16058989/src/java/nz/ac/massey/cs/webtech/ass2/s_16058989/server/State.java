/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package nz.ac.massey.cs.webtech.ass2.s_16058989.server;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.ServletOutputStream;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

/**
 *
 * @author Octet
 */
@WebServlet(name = "State", urlPatterns = {"/ttt/state"})
public class State extends HttpServlet {


    // <editor-fold defaultstate="collapsed" desc="HttpServlet methods. Click on the + sign on the left to edit the code.">
    /**
     * Handles the HTTP <code>GET</code> method.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        
        String format = request.getParameter("format");
        if(format == null) {
            response.sendError(HttpServletResponse.SC_NOT_FOUND);
            return;
        }
        if(!(format.equals("png") || format.equals("txt"))) {
            response.sendError(HttpServletResponse.SC_NOT_FOUND);
            return;
        }
        
        
        HttpSession session = request.getSession(false);
        if(session == null) {
            response.sendError(HttpServletResponse.SC_NOT_FOUND);
            return;
        }
        
        //Sorry for the repetition with getting the board... at this moment in time I found an error at the last minute.
        Board board = (Board) session.getAttribute("board");
        if(board == null) {
            response.sendError(HttpServletResponse.SC_NOT_FOUND);
            return;
        }
        
        ServletOutputStream out = response.getOutputStream();
        out.println((format.equals("txt")) ? (board.display()) : (board.display(true, out, response)));
        
    }

    /**
     * Returns a short description of the servlet.
     *
     * @return a String containing servlet description
     */
    @Override
    public String getServletInfo() {
        return "Serves the current state of the client's game board.";
    }// </editor-fold>

}
